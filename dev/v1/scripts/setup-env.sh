#!/usr/bin/env bash
# One-time environment setup for the Arcade v1 cloud session. Idempotent: it skips what's already installed.
set -euo pipefail
have() { command -v "$1" >/dev/null 2>&1; }
SUDO=""; [ "$(id -u)" -ne 0 ] && have sudo && SUDO=sudo
apt_install() {
  timeout 900 $SUDO apt-get update -o Acquire::Retries=3
  timeout 1800 $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y -o Acquire::Retries=3 "$@"
}
if have apt-get; then
  apt_install build-essential pkg-config curl git jq python3 python3-pip unzip xz-utils file \
    xvfb xauth dbus-x11 at-spi2-core xdotool imagemagick wl-clipboard grim \
    libwebkit2gtk-4.1-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev libssl-dev libsqlite3-dev \
    libxkbcommon-dev libwayland-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
    gstreamer1.0-plugins-good gstreamer1.0-pipewire \
    qt6-base-dev qt6-declarative-dev qt6-wayland qml6-module-qtquick-controls cmake ninja-build \
    sway kwin-wayland mutter ffmpeg tesseract-ocr qpdf libvips-tools zbar-tools fuse3 squashfs-tools \
    clang lld openjdk-17-jdk-headless || echo "some apt packages failed; continuing"
fi
have rustup || { curl -fsSL --retry 3 https://sh.rustup.rs | sh -s -- -y --profile minimal; }
. "$HOME/.cargo/env"
rustup component add clippy rustfmt >/dev/null
for t in cargo-deny cargo-machete cargo-nextest; do have "$t" || cargo install --locked "$t"; done
have node || { curl -fsSL --retry 3 https://deb.nodesource.com/setup_22.x | $SUDO bash - && apt_install nodejs; }
have pnpm || $SUDO npm i -g pnpm@9
if ! have flutter; then
  git clone --depth 1 -b stable https://github.com/flutter/flutter.git "$HOME/flutter"
  echo 'export PATH="$HOME/flutter/bin:$PATH"' >> "$HOME/.bashrc"; export PATH="$HOME/flutter/bin:$PATH"
  flutter config --no-analytics >/dev/null; flutter precache --linux --android
fi
# The Android SDK command-line tools are only needed for the Clipboard spec.
if [ ! -d "$HOME/android-sdk" ]; then
  mkdir -p "$HOME/android-sdk/cmdline-tools" && cd "$HOME/android-sdk/cmdline-tools"
  curl -fsSL --retry 3 -o tools.zip https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
  unzip -q tools.zip && mv cmdline-tools latest && rm tools.zip && cd -
  yes | "$HOME/android-sdk/cmdline-tools/latest/bin/sdkmanager" --licenses >/dev/null || true
  "$HOME/android-sdk/cmdline-tools/latest/bin/sdkmanager" "platform-tools" "platforms;android-35" "build-tools;35.0.0" >/dev/null
fi
echo "Headless Hyprland: built by Link's desktop-e2e workflow (specs/LINK.md §1); not installed here."
echo "setup-env: done"
