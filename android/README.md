# Algo-Mastery Android companion

This is a native Java Android application, not a WebView wrapper. It includes:

- the repository's 56 algorithm modules in a searchable native catalog;
- category filters and local-only bookmarks using `SharedPreferences`;
- detail screens with complexity, source paths, and repository links;
- an offline bubble-sort trace with reset, step, play, and Android back navigation;
- the shared Algo-Mastery dark visual identity and launcher mark.

## Build a debug APK

From this directory:

```sh
./gradlew assembleDebug
```

On Windows use `gradlew.bat assembleDebug`. The generated artifact is:

```text
app/build/outputs/apk/debug/app-debug.apk
```

The debug artifact is signed by the Android Gradle debug keystore, uses package
identifier `com.algomastery.app`, version `0.1.0`, and is suitable for local
installation/testing. It is **not** a public release signature.

Validate the artifact without an emulator:

```sh
aapt dump badging app/build/outputs/apk/debug/app-debug.apk
apksigner verify --verbose app/build/outputs/apk/debug/app-debug.apk
sha256sum app/build/outputs/apk/debug/app-debug.apk
```

## Signed release

Keep the private keystore outside the repository. Configure a `release` signing
block through a local Gradle property or CI secret, then run:

```sh
./gradlew assembleRelease
```

Never commit `keystore.jks`, passwords, or CI credentials. Before publishing,
verify the package, version, signature, and SHA-256 checksum, then upload the
real APK asset to a GitHub Release.
