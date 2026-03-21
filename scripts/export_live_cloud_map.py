#!/usr/bin/env python3
import argparse
import math
import struct
import sys
import time
from pathlib import Path

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2


class CloudMapSaver(Node):
    def __init__(self, topic: str) -> None:
        super().__init__("cloud_map_saver")
        self._msg = None
        self._subscription = self.create_subscription(
            PointCloud2, topic, self._callback, 1
        )

    def _callback(self, msg: PointCloud2) -> None:
        self._msg = msg
        self.get_logger().info(
            f"Received cloud map with width={msg.width}, height={msg.height}"
        )

    @property
    def message(self) -> PointCloud2 | None:
        return self._msg


def resolve_output_path(project_root: Path, output_path: str | None) -> Path:
    cloud_dir = project_root / "cloud_map"
    cloud_dir.mkdir(parents=True, exist_ok=True)
    if output_path:
        path = Path(output_path)
        return path if path.is_absolute() else project_root / path
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return cloud_dir / f"go2_live_cloud_map_{timestamp}.ply"


def extract_points(msg: PointCloud2) -> list[tuple[float, float, float, int, int, int]]:
    field_names = [field.name for field in msg.fields]
    has_rgb = "rgb" in field_names or "rgba" in field_names
    points = []

    if has_rgb:
        rgb_field = "rgb" if "rgb" in field_names else "rgba"
        for point in point_cloud2.read_points(
            msg, field_names=("x", "y", "z", rgb_field), skip_nans=True
        ):
            x, y, z, rgb = point
            if hasattr(rgb, "item"):
                rgb = rgb.item()
            if isinstance(rgb, float):
                if math.isnan(rgb):
                    rgb_int = 0xFFFFFF
                else:
                    rgb_int = struct.unpack("I", struct.pack("f", rgb))[0]
            else:
                try:
                    rgb_int = int(rgb)
                except (TypeError, ValueError):
                    rgb_int = 0xFFFFFF
            r = (rgb_int >> 16) & 0xFF
            g = (rgb_int >> 8) & 0xFF
            b = rgb_int & 0xFF
            points.append((x, y, z, r, g, b))
    else:
        for point in point_cloud2.read_points(
            msg, field_names=("x", "y", "z"), skip_nans=True
        ):
            x, y, z = point
            points.append((x, y, z, 255, 255, 255))

    return points


def write_ascii_ply(path: Path, points: list[tuple[float, float, float, int, int, int]]) -> None:
    with path.open("w", encoding="ascii") as handle:
        handle.write("ply\n")
        handle.write("format ascii 1.0\n")
        handle.write(f"element vertex {len(points)}\n")
        handle.write("property float x\n")
        handle.write("property float y\n")
        handle.write("property float z\n")
        handle.write("property uchar red\n")
        handle.write("property uchar green\n")
        handle.write("property uchar blue\n")
        handle.write("end_header\n")
        for x, y, z, r, g, b in points:
            handle.write(f"{x:.6f} {y:.6f} {z:.6f} {r} {g} {b}\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Save the latched /cloud_map topic to a PLY file."
    )
    parser.add_argument(
        "--topic",
        default="/cloud_map",
        help="PointCloud2 topic to save. Default: /cloud_map",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=20.0,
        help="Seconds to wait for a cloud map message. Default: 20",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Absolute or project-relative PLY path. Default: cloud_map/go2_live_cloud_map_<time>.ply",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    output_path = resolve_output_path(project_root, args.output)

    rclpy.init()
    node = CloudMapSaver(args.topic)

    deadline = time.monotonic() + args.timeout
    while rclpy.ok() and time.monotonic() < deadline and node.message is None:
        rclpy.spin_once(node, timeout_sec=0.2)

    if node.message is None:
        node.get_logger().error(
            f"No PointCloud2 received on {args.topic} within {args.timeout:.1f}s."
        )
        node.destroy_node()
        rclpy.shutdown()
        return 1

    points = extract_points(node.message)
    if not points:
        node.get_logger().error(f"Topic {args.topic} was received but contained 0 valid points.")
        node.destroy_node()
        rclpy.shutdown()
        return 2

    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_ascii_ply(output_path, points)
    node.get_logger().info(f"Saved {len(points)} points to {output_path}")

    node.destroy_node()
    rclpy.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
