# instagram-userfiles-manager

Makes folders per each user from a set of images/videos downloaded from Instagram.

Usernames are recognized through the default name of multimedia content when downloaded from Instagram.

Files must have default name pattern:

```<username>_<numbers>_<numbers>_<numbers>_n.[jpg|mp4]```

If it cannot be detected that way, the application will try to use OCR technology to take it from the multimedia content itself (if it were an Instagram story).

Otherwise, it will move you to a folder named `0_unclassified`.

## Usage

```
python3 main.py [WORKDIR]
```

If `WORKDIR` is not provided, this is the same as the project.
