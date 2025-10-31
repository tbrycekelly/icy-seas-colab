+++
date = "2025-10-28T12:25:00-10:00"
short_text = ""
title = "Common Image Formats Explained"
[[authors]]
    name = "Thomas Bryce Kelly"
    id = "Thomas Bryce Kelly"
    is_member = true
+++

After a recent conversation with a friend about photography and digital images, there seems to be many unanswered questions out there regarding the wide variety of image formats which have become commonplace in our lives. A few months ago I wrote a short article on HDR Photography (link) since so many people were asking questions about that setting on their iPhone. In a similar vein, I hope to build a practical foundation so you know when and why you would like the image to be saved as png, jpg, pdf etc.

### Digital Storage of Sensory Input

Everyone had heard of pixels or megapixels and know that they refer to the little pieces that make up an image, but what most people don’t know is how these pixels relate to bytes, the little pieces of information inside a computer. To make this connection we first need to look a little into optics to understand the basis for all the digital systems.

In elementary school we all learn about the color wheel and how to make green paint by mixing red and blue. In fact, given red, blue, and green (RBG) we can make all the colors by adding together these primary pigments, just as we would paint, to form different colors. Perhaps we’d add a little black to make a shade or a dab of white to get a hue, but you get the picture. Light works this same way, except when we mix all the paints together we ended up with black and when we mix light together we get white. This is because pigments are subtractive while light is additive. In effect we now have two different color systems, both of which are RGB systems.

<figure style="text-align: center;">
  <img src="/2025-image-formats/colors.png" width="200px" alt="RGB color wheel">
  <figcaption>“RBG color wheel” by DanPMK at English Wikipedia. Licensed under CC BY-SA 3.0 via Wikimedia Commons.</figcaption>
</figure>

Just as a theater lighting expert and painters may talk about color in these two different ways, computer systems have a wide variety of systems for doing the same thing. Some of these systems are small changes, like using a slightly different red for a base, and some use very different systems such as hue-saturation-luminance (vs RGB) for their base. Nevertheless, don’t worry about the complexity, we’ll get to each topic in turn.

Now that we have some basic color theory under our belt, let’s move on to image representation.

<figure style="float: right; margin: 0 0 1em 1em; text-align: center;">
  <img src="/2025-image-formats/pixelgrid.jpg" width="150px" alt="tulip in a grid">
  <figcaption style="font-size: 0.9em; color: #666; max-width: 150px;">
    Picture of tulip made up of pixels.
  </figcaption>
</figure>

Besides pixels, images can be stored in other ways as well. Images, like photographs, that are made up of pixels are also known as Raster files, which means that they are all structured in a particular way. In Raster files the contents are stored as an array of grid cells with a piece of data stored in each cell. For example the grid shown here has some cells filled in while others are not. Each grid cell is a pixel, and if we are using the RGB scheme then each pixel also has three values associated with it. The pixels that make up the flower would contain the data (R = 1, G = 0, B = 0) where as the stem would contain (R = 0, G = 1, B = 0).

This works very well for files or images that are of fixed size and data composition; but for files of a less-regular sort, you may not want to be constrained by a grid. In these files, often called Vector formats, the data is stored based on its coordinates within the file. In order words, imagine looking up the location of the Capital Building on a map. Given a grid I could tell you that the capital building is at K4 and this would be a Raster format. Using this grid, there is no way to be more specific than K4 even if the Capital Building is on the left side of K4.

If we were using a Vector format then the we might store the locations in Latitude/Longitude. The location would then be 38°53′23.29″N by 77°00′32.81″W. Notice that I can be as precise as I want here by simply making the decimals longer (and the file size larger). To make an image using this technique, every line and every ‘brush stroke’ would be stored which makes it well suited to line diagrams and simple graphics. Creating photo-realistic pictures is not quite as easy.  Already I hope some of the trade-offs of these two systems are becoming clear. 

<figure style="text-align: center;">
  <img src="/2025-image-formats/progressive-zoom.png" width="600px" alt="raster-based zoom in onto a graph">
  <img src="/2025-image-formats/progressive-zoom2.png" width="600px" alt="vector-based zoom in onto a graph">
  <figcaption>“Comparison of a raster image format (top, png) and a vector image format (bottom, pdf). Notice the aliasing of the black line in the top image due to the lack of pixel resolution for the line.</figcaption>
</figure>

While the vast majority of photos, pictures and images are stored using a raster format, vector formats certainly have their place. The most common format which uses a vector format–and one we’re all familiar with–is the PDF. PDF, or Portable Document Format, stores all the data in the file as relative locations within the document (think x-y coordinates). Have you ever zoomed into a PDF document before and found that it doesn’t get blurry no matter how far you go[1]?

### Lossless and Lossy Compression
It would be impossible to appreciate the variety of image formats in use today without knowing their tradeoffs, and this requires a discussion on data compression. While I have personally always found the idea of taking a file of size X and being able to shrink it to a smaller size thrilling, I also recognize that most people probably do not. Therefore, let’s stick to the basic and the necessary in our exploration.

The techniques used in data compression can always be separated into two distinct classes, one termed ‘Lossless’ and the other as ‘Lossy’. In Lossless compression, the resulting, compressed file contains an exact copy of the original data repacked and manipulated in reversible ways. In other words, if you compress file ‘A’ and then decompress it, the result is a perfect copy of ‘A’. Lossy compression, by comparison, does not permit this perfect reproduction; and as its name implies, some data is lost through the act of compressing the file.

While these names are straightforward, it can seem a bit disingenuous to have a Lossy data compression technique. For example, take a 4 page essay and compress it down to 2 pages. Either you can shrink the text down so that it fits or you can throw away the last two pages. Now while this may seem to illustrate the concepts of lossless and lossy compression, in reality it doesn’t. The central principle used in Lossy compression is the removal of the least significant information. Rather than simply discarding those two pages, in lossy compression we might remove all the spaces, indents and punctuation to make the text all fit. This still isn’t a perfect example, but we’ll see how this works in practice.

<figure style="float: left; margin: 1em 1em 1em 1em; text-align: center;">
  <img src="/2025-image-formats/spectral-response.gif" width="450px" alt="spectral response of the eye">
  <figcaption style="font-size: 0.9em; color: #666; max-width: 450px;">
    Graph of spectral response of human retina cells (i.e. sensitivity). Image from www.cs.cf.ac.uk
  </figcaption>
</figure>

Human perception of color is far from perfect; just consider the recent blue versus white dress phenomenon. Some of our biases can be explained by the response spectrum of our retina cells wherein our eyes are more sensitive to red and green than to blue. This helps to explain why blue colors are considered “dark” while orange, yellow and green are “bright” colors. Needless to say, there are also numerous other biological and psychological factors that influence our perception of colors.

Putting this all together, image formats such as JPEG can actually selectively remove information in the pixels to make the image more compressable. Just as it takes less information to store the number 3.14 than 3.1415926535, the JPEG image model decides what level of compromise is appropriate to leave behind a reasonable approximation (or lossy) version of the original.

While it may not seem like it, it is this simple compromise that allows JPEG images to be much smaller than other formats under a range of general circumstances. Since this lossy method is best suited for images where the loss is not noticeable, it is especially useful in photographs where natural variation is extremely high and where a slightly different color would not be obvious.

Virtually all photographs are stored in JPEG format, and therefore undergo a small loss of detail compared to the ‘true’ original (hence the use of RAW format in high end cameras), while at the same time images of logos or text documents are not stored as JPEGs since their uniform color and lack of ‘noise’ make the lossy encoding process very obvious.

Another format that does this “color elimination” is the classic GIF image format made infamous for its use on websites and by early versions of Windows. It is a lossless, raster format but whose color pallet is limited to just 256 colors. Rather than the PNG color pallet of over 16,000,000 (or 4.6 billion for 24 bit and 32 bit, respectively). the GIF format was developed in the early 90’s when internet bandwidth was quite limited. As a result, this highly compressed image format simply cut down the number of bits per pixel to 8 (hence $2^8=256$). The 8 bit pallet it uses can be one of several standard sets (e.g. the Web pallet).


<figure style="text-align: center;">
  <img src="/2025-image-formats/palette-comparison.png" width="90%" alt="comparison between different resolutions of color fidelity">
  <figcaption>From left to right: Gif with web pallet (fixed set of 256 colors). Original JPG image with 24 bits of color depth. GIF with internal pallet stored as a lookup table (limited to 256 colors).</figcaption>
</figure>

GIF does have one trick up its sleeve: it can store a lookup table of 256 colors within the file so that if you have an image with 256, non-standard colors, the image can be stored without loss. See the image set above for an example of these pallets.

### Contemporary, popular formats
So which formats are you likely to deal with from day to day. JPEG is certainly a front runner with all those family photos, but with more and more of our lives spent in the digital space its predominance is losing ground. PNG is omnipresent on the web whenever you see logos and other text-heavy images. In fact, when you take a screenshot, the result is a PNG. PDFs are commonplace but often embedded with JPEGs and other formats making a clear delineation difficult. Ultimately there is not one best format for all usage cases, and in fact every format does have a best usage case where it offers the best features and the lowest tradeoffs.

I hope this overview of image formats and storage techniques has been helpful in navigating the alphabet soup. Perhaps this information will make the choice as to which format to save an image as an easier one.