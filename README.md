# Font Icon Creator

With this tool you can create you own icons font from images for you web page. You can use PNG, JPG or SVG images.

The basic usage is:
```
docker run -v `pwd`/icons:/src -e FONT_NAME=lolo wixet/font-icon-generator
```
where `icons` directory contains a set of images. It will create in the same directory the fonts and the css file.


# Negate option

The expected input is a black picture over a white background. If you case is the opposite, just use the negate option:
```
docker run -v `pwd`:/src -e FONT_NAME=lolo -e NEGATE=true wixet/font-icon-generator
```

# Keeping the SVG files

If you are using non svg files, an intermediate process of converting your file into svg is done. If for some reason you want to keep them, just mount the `/svg` directory:

```
docker run -v `pwd`:/src -v `pwd`/svg:/svg -e FONT_NAME=lolo wixet/font-icon-generator
```
With this command, the converted SVG files will be stored in your host machine


# What to do with the generated files

The fonts and the css file is generated. You have to cofigure the `css` file depending on the location in your webpage.
Where the fonts are loaded, for example the line `url('/assets/fonts/lolo.eot');` you should replace `/assets/fonts/lolo.eot` by the real location. In my
case I use `angular` and this is the default path for me. What you put there is what the browser will try to downoad so a fast and easy way to test it is
just pasting it into the browser and check that the font is being downloaded.

The next step is to include the `css` (or its content) into your webpage and in your use it in your `html` code. For example
```
<i class="icon-back"></i>
```
in case you have an icon called `back`. Remember that the icon name is `icon-{name}` where `{name}` is the origial icon filename without the extension. So for the
case `<i class="icon-back"></i>` it is because I have a file called `back.png`.

# Build

If you want to build the container because you want your own customized version, just pull the repo and run docker
```
docker buildx build -t my-font-gen . --load
```
and then
```
docker run -v `pwd`:/src -e FONT_NAME=lolo my-font-gen
```

# Under the hood

All the work is done by other libraries, this script just connect them.

* [potrace](https://potrace.sourceforge.net/) to create SVG files from bitmaps
* [imagemagick](https://github.com/ImageMagick/ImageMagick) image preprocessing to create `potrace` compatible images
* [fontforge](https://github.com/fontforge/fontforge) to create the font from SVG files


# Troubleshooting

If your format is other than SVG, a conversion is performed. This process may cause some troubles depending on your source files, if the resulting image is completely black or white these are the most common reasons:

* The SVG conversion expects a black and white image and if more colors are present, they are converted into black and white. Try to manually set the images to black and white
* The normal case is a black picture over a white background. If your picture is white over a black background try the `negate` option
* Transparent background is converted into a white one. If your source image is a white picture over a transparent background try the `negate` option
