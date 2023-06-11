# Building instructions
-   [Galton Board](#galton-board)
-   [Preparation](#preparation)
    -   [Tools](#tools)
    -   [Material](#material)
    -   [Prior knowledge](#prior-knowledge)
-   [Building instructions](#building-instructions)
    -   [Galton Board](#galton-board)
	    - [Base frame](#base-frame)
	    -  [Box](#box)
	    - [Slide](#slide)
	- [Marble lift](#marble-lift)
	- [Stepper engine](#stepper-engine)
	- [RasberryPi](#rasberrypi)
		- [Circuit board](#circuit-board)
		- [RasberryPi holder](#rasberrypi-holder)
		- [Sensor system](#sensor-system)
-   [Improvement ideas](#improvement-ideas)
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
<details open>
<summary>All parts:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/915d561c-c3d3-44ae-94d4-0f3e04ff7e47" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/1739643b-7f57-4d11-be28-5f685a05bd5b" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/3ab6cf73-3f96-48e3-b5fe-28cb901156bb" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/926411bf-fedd-43a8-ae7b-ab1cb4935aa6" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/245b9572-7db1-4151-bf3e-87b08a82bd01" width="450" height="600">
</details>

<br>

#### Base Frame

Arrange the parts as shown in the picture, ensuring everything is easily accessible. Glue the prongs together on both sides using wood glue. Repeat this step for each side. Depending on the color of the MDF, you can decide which side should face the front.

<details open>
<summary>The procedure is as follows:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/915d561c-c3d3-44ae-94d4-0f3e04ff7e47" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/19de83af-eb2f-4838-9a40-a15c786c2613" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/4991c0ec-d9f3-40dc-9465-27d20b7f6204" width="450" height="600">
</details>
<br>
The acrylic plate from the Glass.svg file serves as the lid for the Galton board. However, this is the final step after everything else has been installed on the board.

**Tip**: The acrylic board and the MDF should not be glued together. This allows you to remove the board whenever necessary for maintenance. Additionally, acrylic and MDF do not bind well when glued.
<br>
Next, we move to the end piece at the bottom, where the marbles land and roll out. This step is straightforward.

<details open>
<summary>The process is as follows:</summary>
<br>
<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/69453948/244934054-1739643b-7f57-4d11-be28-5f685a05bd5b.jpg" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/153efc1d-5f52-4e13-896e-d0969e6bbb5b" width="450" height="600">
</details>


Simply glue the pieces on top of each other, allowing time for the wood glue to dry between layers. Try to ensure the layers are glued as straight as possible.

**Tip:** If there are any unevenness in the end piece, you can correct it by sanding it straight.

At the end of both processes, you can combine them together. The combined result should look like this:
<details open>
<summary>Combination:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/4f26dd0e-27ba-468c-8f7b-108c0a0a37ee" width="450" height="600">
</details>
<br>

#### Box
Now we come to the building instructions for the box located beneath the Galton board. The process is similar to building the Galton board. 

<details open>
<summary>The process is as follows:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/926411bf-fedd-43a8-ae7b-ab1cb4935aa6" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/d7e26d13-acc1-479e-bb83-f738e0371fc7" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/f2785eb2-9703-4d59-830b-63b7d19692a7" width="450" height="600">
</details>

However, note that the lid should not be glued down yet. This will allow you to lay the cables later. The box is already stable enough with just one side glued.

#### Slide
Finally, we move on to the slide, which connects the board with the lift. A file is still needed for this step.

<details open>
<summary>Please refer to the following pictures:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/038c0740-8308-476b-816b-9900cbc0a092" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/32db61c6-c3fd-4583-844a-01c3ced091a4" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/19798f32-c7fb-4b4a-979b-5b8787b26b47" width="450" height="600">
</details>

With all four parts, it doesn't need to be filed very steeply, but it is important that it has a straight angle. 

Once that is done, you can assemble these parts together, resulting in the following configuration:

<details open>
<summary>Configuration:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/640d932a-ad56-4629-8982-a79a543e81e6" width="450" height="600">
</details>

After assembling the slide, you can also glue the "funnel" at the end of the slide. It should look something like this:

<details open>
<summary>Configuration:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/ce61bb0b-3611-4fc6-a9ec-126f3a709cf3" width="450" height="600">
</details>

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

<details open>
<summary>Sensor system:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/66927b07-3723-4440-8e28-be69d0ad9c5f" width="450" height="600">
</details>

The picture shows an aligned (below) and an unaligned (above) laser. For the top photodiode, only the power indicator light is on, but the laser signal light is off.
The acrylic glass can be added to the system. It is important that the glass is not glued or
fixed to the rest of the Galton Board.
## Improvement ideas
TODO
