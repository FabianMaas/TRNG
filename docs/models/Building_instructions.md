# Building instructions

-   [Galton Board](Galton-Board)
-   [Preparation](Preparation)
    -   [Tools](Tools)
    -   [Material](Material)
    -   [Prior knowledge](Prior-knowledge)
-   [Building instructions](Building-instructions)
    -   [Galton Board](Galton-Board)
	    - [Base frame](Base-frame)
	    -  [Box](Box)
	    - [Slide](Slide)
	- [Marble lift](Marble-lift)
	- [Stepper engine](Stepper-engine)
	- [RasberryPi](RasberryPi)
		- [Circuit board](Circuit-board)
		- [RasberryPi holder](RasberryPi-holder)
		- [Sensor system](Sensor-system)
-   [Improvement ideas](Improvement-ideas)
---
## Galton Board
Kurze Einführung was es überhaupt ist TODO

## Preparation
### Tools
- Laser cutter
- 3D printer
- Superglue
- Soldering iron
- Sandpaper and file
- Screwdriver or drill
- Screws
- Pliers

### Material

<table>
    <tr>
      <th>Material</th>
      <th>Anzahl/Maße</th>
    </tr>
  <tbody>
    <tr>
      <td>MDF</td>
      <td>???</td>
    </tr>
    <tr>
      <td>ABS</td>
      <td>???</td>
    </tr>
        <tr>
      <td>PLA</td>
      <td>???</td>
    </tr>
        <tr>
      <td>Acryl</td>
      <td>???</td>
    </tr>
        <tr>
      <td>Metal rod</td>
      <td>2x 2,1cm</td>
    </tr>
        <tr>
      <td>RasberryPi</td>
      <td>1x, ...</td>
    </tr>
        <tr>
      <td>Stepper engine</td>
      <td>1x, ...</td>
    </tr>
        <tr>
      <td>Laser</td>
      <td>4x, ...</td>
    </tr>
        <tr>
      <td>Photodiodes</td>
      <td>4x, ...</td>
    </tr>
            <tr>
      <td>Tube</td>
      <td>???</td>
    </tr>
            <tr>
      <td>Height-adjustable feet</td>
      <td>4x</td>
    </tr>
            <tr>
      <td>Marbles</td>
      <td>40x, 14mm</td>
    </tr>
    
  </tbody>
</table>

### Prior knowledge
The following instructions require previous knowledge of how to use the laser cutter and
the 3D printer as well as experience in soldering.
Basic manual skills are recommended.

---
## Building instructions
### Galton Board

The first thing to do is to cut the following SVG files. The materials used for this project are MDF and acrylic, with MDF being the primary material. Both materials have a thickness of 3mm and should be cut to the exact dimensions specified in the sketches.

Make sure that the acrylic that you use is transparent. You can also remove the logo or add your own logo.
<br>
The following SVG files should be printed on MDF:

- Prototype.svg
- UnderBox.svg
- TODO

The SVG file for the acrylic material is:

- Glass.svg

After cutting all the components, you will have the following parts:
!!!BILDER HINZUFÜGEN!!!



#### Base Frame

Arrange the parts as shown in the picture, ensuring everything is easily accessible. Glue the prongs together on both sides using wood glue. Repeat this step for each side. Depending on the color of the MDF, you can decide which side should face the front.

The procedure is as follows:
!!!BILDER HINZUFÜGEN!!!

The acrylic plate from the Glass.svg file serves as the lid for the Galton board. However, this is the final step after everything else has been installed on the board.

**Tip**: The acrylic board and the MDF should not be glued together. This allows you to remove the board whenever necessary for maintenance. Additionally, acrylic and MDF do not bind well when glued.
<br>
Next, we move to the end piece at the bottom, where the balls land and roll out. This step is straightforward. The process is as follows:

!!!BILDER HINZUFÜGEN!!!

Simply glue the pieces on top of each other, allowing time for the wood glue to dry between layers. Try to ensure the layers are glued as straight as possible.

**Tip:** If there are any unevenness in the end piece, you can correct it by sanding it straight.

#### Box
Now we come to the building instructions for the box located beneath the Galton board. The process is similar to building the Galton board. The process is as follows:

!!!BILDER HINZUFÜGEN!!!

However, note that the lid should not be glued down yet. This will allow you to lay the cables later. The box is already stable enough with just one side glued.

#### Slide
Finally, we move on to the slide, which connects the board with the lift. A file is still needed for this step. Please refer to the following pictures:

!!!BILDER HINZUFÜGEN!!!

With all four parts, it doesn't need to be filed very steeply, but it is important that it has a straight angle. 

Once that is done, you can assemble these parts together, resulting in the following configuration:

!!!BILDER HINZUFÜGEN!!!

After assembling the slide, you can also glue the "funnel" at the end of the slide. It should look something like this:

**Tip:** Ensure that the funnel is tight enough at the end to accommodate exactly one marble on the back wall.
### Marble lift
TODO
### Stepper engine
TODO
### RasberryPi
TODO
#### Circuit board
TODO
#### RasberryPi holder
TODO
#### Sensor system
In this step, the sensors are installed.
The two brackets for the laserdiodes are filled with two laserdiodes each bracket and are
glued into the middle of the Galton Board. The four photodiodes are clipped into their
designated sockets and plugged into the sides of the Galton board.
For the next step, both the lasers and the photodiodes must be connected to the power supply.
The photodiodes have an indicator light that lights up when a laser signal is received. Now
the lasers and photodiodes have to be aligned with each other. The lasers inside and the
photodiodes with their brackets are moved slightly until the control lamp lights up. As soon as all four lights are lit, the brackets are glued in this position to the outer side of the Galton Board and the lasers are held in their position on the inside.

!!!BILDER HINZUFÜGEN!!!

The picture shows an aligned (below) and an unaligned (above) laser. For the top photodiode, only the power indicator light is on, but the laser signal light is off.
The acrylic glass can be added to the system. It is important that the glass is not glued or
fixed to the rest of the Galton Board.
## Improvement ideas
TODO
