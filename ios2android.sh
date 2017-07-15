#!/bin/bash

# ios2android - a simple script to port iOS retina images to the appropriate Android density buckets

# The MIT License (MIT)

# Copyright (c) 2013 Ninjanetic Design Inc.
# Copyright (c) 2014 Matteo Piotto

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Requires Imagemagick
# To install on Mac: brew install imagemagick

# Floating point number functions from http://www.linuxjournal.com/content/floating-point-math-bash

#####################################################################
# Default scale used by float functions.

float_scale=2

#####################################################################
# Evaluate a floating point number expression.

function float_eval()
{
    local stat=0
    local result=0.0
    if [[ $# -gt 0 ]]; then
        result=$(echo "scale=$float_scale; $*" | bc -q 2>/dev/null)
        stat=$?
        if [[ $stat -eq 0  &&  -z "$result" ]]; then stat=1; fi
    fi
    echo $result
    return $stat
}

#####################################################################
# Delete all non retina images
#ls -l -I "*2x.*" -I "*.sh" | awk -F' ' '{print $9}' | xargs rm -f

#####################################################################
# Process images.

rm -rf drawable-mdpi
rm -rf drawable-hdpi
rm -rf drawable-xhdpi
rm -rf drawable-xxhdpi
mkdir drawable-mdpi
mkdir drawable-hdpi
mkdir drawable-xhdpi
mkdir drawable-xxhdpi

for ii in *2x.jpg *2x.png; do 
    if [ -f "$ii" ];
    then
        if [[ ${ii} =~ ~ipad ]]; then
            x=${ii/@2x~ipad./.}
            x=${x//[- ]/_}

            if [[ ${x} =~ ^[0-9] ]]; then
                x="img_${x}"
            fi

            x=`echo $x | tr "[:upper:]" "[:lower:]"`
            echo $ii 
            convert -resize 50% "$ii" drawable-large-mdpi/$x
            convert -resize 75% "$ii" drawable-large-hdpi/$x
            convert -resize 112.5% "$ii" drawable-large-xhdpi/$x 

            if [ $# -gt "0" ]; then
                # if a parameter is specified, use it as a pre-scaling value to create images targeted for phones
                mdpi=$(float_eval "50 * ${1}")
                hdpi=$(float_eval "75 * ${1}")
                xhdpi=$(float_eval "112.5 * ${1}")
                xxhdpi=$(float_eval "150 * ${1}")
                convert -resize $mdpi% "$ii" drawable-mdpi/$x
                convert -resize $hdpi% "$ii" drawable-hdpi/$x
                convert -resize $xhdpi% "$ii" drawable-xhdpi/$x 
                convert -resize $xxhdpi% "$ii" drawable-xxhdpi/$x 
            fi
        else
            x=${ii/@2x./.}
            if [[ ${x} =~ -568h ]]; then
                x=${x/-568h./.}
            fi
            x=${x//[- ]/_}

            if [[ ${x} =~ ^[0-9] ]]; then
                x="img_${x}"
            fi

            x=`echo $x | tr "[:upper:]" "[:lower:]"`
            echo $ii
            convert -resize 50% "$ii" drawable-mdpi/$x
            convert -resize 75% "$ii" drawable-hdpi/$x
            convert -resize 112.5% "$ii" drawable-xhdpi/$x 
        fi
    fi
done
