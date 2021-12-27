#!/usr/bin/env bash

set -Eeuo pipefail
trap cleanup SIGINT SIGTERM ERR EXIT

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)

usage() {
  cat << EOF
Usage: $(basename "${BASH_SOURCE[0]}") [-h] [-v] --profile staging commands

Available options:

-h, --help        Print this help and exit
-v, --verbose     Print script debug info
-p, --profile     Set the deployment profile
EOF
  exit
}

cleanup() {
  trap - SIGINT SIGTERM ERR EXIT
  # script cleanup here
}

msg() {
  echo >&2 -e "${1-}"
}

die() {
  local msg=$1
  local code=${2-1} # default exit status 1
  msg "$msg"
  exit "$code"
}

parse_params() {
  # default values of variables set from params
  flag=0
  param=''

  while :; do
    case "${1-}" in
    -h | --help) usage ;;
    -v | --verbose) set -x ;;
    --no-color) NO_COLOR=1 ;;
    -p | --profile)
      profile="${2-}"
      shift
      ;;
    -?*) die "Unknown option: $1" ;;
    *) break ;;
    esac
    shift
  done

  commands=("$@")

  # check required params and filenames
  [[ -z "${profile-}" ]] && die "Missing required parameter: profile"
  [[ ${#commands[@]} -eq 0 ]] && die "Missing commands"

  return 0
}

parse_params "$@"

# script logic

function prepare_kube_context() {
  echo "INFO - Prepare kubectl context..."
  export KUBECONFIG=$(mktemp)
  echo "
---
apiVersion: v1
kind: Config
clusters:
  - name: kube
    cluster:
      certificate-authority-data: ${KUBERNETES_CA}
      server: ${KUBERNETES_API_SERVER}
contexts:
  - name: kube
    context:
      cluster: kube
      user: kube
users:
  - name: kube
    user:
      token: ${KUBERNETES_TOKEN}
current-context: kube" > $KUBECONFIG
}

function precheck_profile() {
  echo "INFO - Preckeck selected profile..."
  if [[ $profile == "staging" ]]; then
      if [[ $(git rev-parse --abbrev-ref HEAD | sed 's/[^a-zA-Z0-9]/-/g') == "main" ]]; then
          die "Wrong profile for branch!" 1
      fi
  fi
  echo "INFO - Selected profile is ${profile}!"
}

function generate_release_name() {
  CHECK=$(echo $GIT_BRANCH || true)
  if [[ -z "${CHECK}" ]]; then
    echo $(git rev-parse --abbrev-ref HEAD | sed 's/[^a-zA-Z0-9]/-/g')
  else
    echo $(echo $GIT_BRANCH | sed 's/[^a-zA-Z0-9]/-/g')
  fi
}

function prepare_profile() {
  release_name=$(generate_release_name)
  echo "INFO - Prepare profile for ${profile}..."
  echo "INFO - Generated release name is ${release_name}!"

  export SKAFFOLD_PROFILE=$profile

  if [[ $profile == "staging" ]]; then
      export RELEASE_NAME="staging-${release_name}"
      export RELEASE_NAMESPACE=hafenmeister
      export RELEASE_HOSTNAME="${release_name}.staging.hafenmeister.io"
  fi
}

# Precheck the selected profile
precheck_profile

# Prepare the kubectl config file
prepare_kube_context

# Prepare profile
prepare_profile

exec ${commands[@]}
