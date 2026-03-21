#!/usr/bin/env sh

_rtabmap_stack_prefix="${COLCON_CURRENT_PREFIX:-${AMENT_CURRENT_PREFIX:-}}"
if [ -z "${_rtabmap_stack_prefix}" ]; then
  return 0 2>/dev/null || exit 0
fi

_rtabmap_stack_workspace_root=""
for _rtabmap_stack_candidate in \
  "${_rtabmap_stack_prefix}/.." \
  "${_rtabmap_stack_prefix}/../.."
do
  _rtabmap_stack_candidate_root="$(cd "${_rtabmap_stack_candidate}" 2>/dev/null && pwd)"
  _rtabmap_stack_candidate_install_dir="${_rtabmap_stack_candidate_root}/vendor/rtabmap_stack/rtabmap-0.23.4/install"

  if [ -f "${_rtabmap_stack_candidate_install_dir}/lib/rtabmap-0.23/RTABMapConfig.cmake" ]; then
    _rtabmap_stack_workspace_root="${_rtabmap_stack_candidate_root}"
    break
  fi
done

if [ -z "${_rtabmap_stack_workspace_root}" ]; then
  unset _rtabmap_stack_prefix
  unset _rtabmap_stack_workspace_root
  return 0 2>/dev/null || exit 0
fi

_rtabmap_stack_install_dir="${_rtabmap_stack_workspace_root}/vendor/rtabmap_stack/rtabmap-0.23.4/install"
_rtabmap_stack_config_dir="${_rtabmap_stack_install_dir}/lib/rtabmap-0.23"
_rtabmap_stack_config_file="${_rtabmap_stack_config_dir}/RTABMapConfig.cmake"

_rtabmap_stack_prepend_unique() {
  _rtabmap_stack_var_name="$1"
  _rtabmap_stack_value="$2"
  eval _rtabmap_stack_current_value=\"\${${_rtabmap_stack_var_name}:-}\"

  case ":${_rtabmap_stack_current_value}:" in
    *":${_rtabmap_stack_value}:"*) return 0 ;;
  esac

  if [ -n "${_rtabmap_stack_current_value}" ]; then
    eval export "${_rtabmap_stack_var_name}=${_rtabmap_stack_value}:${_rtabmap_stack_current_value}"
  else
    eval export "${_rtabmap_stack_var_name}=${_rtabmap_stack_value}"
  fi
}

if [ -f "${_rtabmap_stack_config_file}" ]; then
  export RTABMap_DIR="${_rtabmap_stack_config_dir}"
  _rtabmap_stack_prepend_unique CMAKE_PREFIX_PATH "${_rtabmap_stack_install_dir}"
  _rtabmap_stack_prepend_unique LD_LIBRARY_PATH "${_rtabmap_stack_install_dir}/lib"
  _rtabmap_stack_prepend_unique PATH "${_rtabmap_stack_install_dir}/bin"
fi

unset _rtabmap_stack_prefix
unset _rtabmap_stack_workspace_root
unset _rtabmap_stack_candidate
unset _rtabmap_stack_candidate_root
unset _rtabmap_stack_candidate_install_dir
unset _rtabmap_stack_install_dir
unset _rtabmap_stack_config_dir
unset _rtabmap_stack_config_file
