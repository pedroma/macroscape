#!/usr/bin/env python

# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex,csv
# The simplestyle module provides functions for style parsing.
from simplestyle import formatStyle

class HelloWorldEffect(inkex.Effect):
    """
    Example Inkscape effect extension.
    Creates a new layer with a "Hello World!" text centered in the middle of the document.
    """
    def __init__(self):
        """
        Constructor.
        Defines the "--what" option of a script.
        """
        # Call the base class constructor.
        inkex.Effect.__init__(self)

        # Define string option "--what" with "-w" shortcut and default value "World".
        self.OptionParser.add_option('-f', '--filename', action = 'store',
          type = 'string', dest = 'data_file',
          help = 'File to get data from?')

    def effect(self):
        """
        Effect behaviour.
        Overrides base class' method and inserts "Hello World" text into SVG document.
        """
        self.parse()
        # Get script's "--what" option value.
        data_file = self.options.data_file

        try:
            handler = csv.reader(open(data_file,'r'))

            for line in handler:
                id,txt = line

                # Create text element
                text = inkex.etree.Element(inkex.addNS('text','svg'))
                text.text = txt

                node = self.getElementById(id)
                # Again, there are two ways to get the attibutes:
                width  = inkex.unittouu(node.get('width'))
                height = inkex.unittouu(node.get('height'))

                xpos = inkex.unittouu(node.get('x'))
                ypos = inkex.unittouu(node.get('y'))

                # Set text position to center of document.
                text.set('x', str(xpos + (width/2)))
                text.set('y', str(ypos + (height/2)))

                # Center text horizontally with CSS style.
                style = {'text-align' : 'center', 'text-anchor': 'middle'}
                text.set('style', formatStyle(style))

                # Connect elements together.
                self.document.getroot().append(text)
        except:
            inkex.errormsg("Unkown error")

# Create effect instance and apply it.
effect = HelloWorldEffect()
effect.affect()
