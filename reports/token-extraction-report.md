# Xnet Token Extraction Report

Source: Android theme library only.

## Parsed Files

- `xnet_hub_theme/src/main/res/values/colors.xml`
- `xnet_hub_theme/src/main/res/values/themes.xml`
- `xnet_hub_theme/src/main/res/values/styles.xml`
- `xnet_hub_theme/src/main/res/values/attrs.xml`
- `xnet_hub_theme/src/main/res/drawable/*.xml`

## Theme Variants

- `classic-light` from `Theme.XnetCore.Light`
- `classic-dark` from `Theme.XnetCore.Dark`
- `cyber-green` from `Theme.XnetCore.CyberGreen`
- `cyber-blue` from `Theme.XnetCore.CyberBlue`
- `cyber-black` from `Theme.XnetCore.CyberBlack`
- `cyber-orange` from `Theme.XnetCore.CyberOrange`
- `cyber-rgb` from `Theme.XnetCore.CyberRGB`

## Drawable XML Resources

- Parsed `57` drawable XML files.
- Stored under `resources.drawables` in `tokens/tokens.json`.
- Each drawable includes source path, root type, tag counts, root attrs, and XML node attrs.

## Next Extraction Targets

- Promote repeated drawable sizes/radii into stable semantic component tokens.
- Decide whether Java hard-coded fallback colors should become public semantic tokens.
- Add generated Android XML, Web CSS, and future Swift token outputs from this JSON.
