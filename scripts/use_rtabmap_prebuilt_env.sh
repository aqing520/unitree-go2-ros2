#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RTABMAP_INSTALL_DIR="$ROOT_DIR/vendor/rtabmap_stack/rtabmap-0.23.4/install"
RTABMAP_CONFIG_DIR="$RTABMAP_INSTALL_DIR/lib/rtabmap-0.23"
RTABMAP_CONFIG_FILE="$RTABMAP_CONFIG_DIR/RTABMapConfig.cmake"
RTABMAP_VERSION_FILE="$RTABMAP_CONFIG_DIR/RTABMapConfigVersion.cmake"

prepend_unique() {
  local var_name="$1"
  local value="$2"
  local current="${!var_name:-}"

  case ":${current}:" in
    *":${value}:"*) return 0 ;;
  esac

  if [[ -n "$current" ]]; then
    export "${var_name}=${value}:${current}"
  else
    export "${var_name}=${value}"
  fi
}

if [[ ! -d "$RTABMAP_INSTALL_DIR" ]]; then
  echo "[ERROR] RTAB-Map prebuilt install not found: $RTABMAP_INSTALL_DIR" >&2
  return 1 2>/dev/null || exit 1
fi

if [[ ! -f "$RTABMAP_CONFIG_FILE" ]]; then
  echo "[ERROR] RTABMapConfig.cmake not found: $RTABMAP_CONFIG_FILE" >&2
  return 2 2>/dev/null || exit 2
fi

if [[ ! -f "$RTABMAP_VERSION_FILE" ]]; then
  echo "[ERROR] RTABMapConfigVersion.cmake not found: $RTABMAP_VERSION_FILE" >&2
  return 3 2>/dev/null || exit 3
fi

if ! grep -Eq 'PACKAGE_VERSION[[:space:]]+"0\.23\.4"' "$RTABMAP_VERSION_FILE"; then
  echo "[ERROR] Expected RTAB-Map 0.23.4 in $RTABMAP_VERSION_FILE" >&2
  return 4 2>/dev/null || exit 4
fi

export RTABMap_DIR="$RTABMAP_CONFIG_DIR"
prepend_unique CMAKE_PREFIX_PATH "$RTABMAP_INSTALL_DIR"
prepend_unique LD_LIBRARY_PATH "$RTABMAP_INSTALL_DIR/lib"
prepend_unique PATH "$RTABMAP_INSTALL_DIR/bin"

echo "[OK] RTABMap_DIR=$RTABMap_DIR"
echo "[OK] Using prebuilt RTAB-Map install: $RTABMAP_INSTALL_DIR"
