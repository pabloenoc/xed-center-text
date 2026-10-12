# Xed Center Text Plugin

This is a plugin for centering markdown text in the Xed text editor. It's like [Olivetti mode](https://github.com/rnkn/olivetti) on Emacs.

## Installation

1. Download the `center-text` directory from above. You can click on the green `Code` button here on GitHub and then select `Download as ZIP`. It will save the repository as `xed-center-text-master`. Extract the files.

2. Go to `~/Downloads/` or wherever you extracted the files with `cd ~/Downloads`. 

2. Create your `plugins` directory if it doesn't exist, and copy the plugin to your `plugins` directory:

```bash
  mkdir -p ~/.local/share/xed/plugins
  cp -r center-text ~/.local/share/xed/plugins/
```

## Usage

Access Xed's configuration dialog via `Edit | Preferences | Plugins`, and enable the plugin. 

You can customize the text width by clicking on `Preferences`. The default value is 72.

## Development References

Take a look at these repos for plugin development reference:

- https://github.com/gabriellaraujocoding/xed-extra-plugins
- https://github.com/macp3o/xed-linespacing/tree/master


## License

Xed Center Text Plugin is released under the [MIT License](https://opensource.org/license/MIT).





