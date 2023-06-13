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
	- [Stepper motor](#stepper-motor)
	- [RasberryPi](#rasberrypi)
		- [Circuit board](#circuit-board)
		- [RasberryPi holder](#rasberrypi-holder)
		- [Sensor system](#sensor-system)
-   [Improvement ideas](#improvement-ideas)
---
## Galton Board
Our variation of a galton board uses only two compartments instead of many. Every pin inside a galton board has a 0.5 change to be left or right. We use this uniform distribution to generate binary-valued random numbers. Our board has two stages with one pin per stage. Each compartment on each stage produces a bit, either a zero or a one. We use plastic marbles which run trough the system and interrupt laser which are pointed onto sensors. In the end they will get pumped up to the top again with a piston lift.

<p align="center">
  <img src="https://github.com/FabianMaas/TRNG/assets/129375472/ac940497-4d91-4675-92ab-4f59bd2f3b6b">
</p>

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
      <th>Count
      <th>Measures</th>
    </tr>
  <tbody>
    <tr>
      <td>MDF</td>
      <td>1</td>
      <td>605x550 mm</td>
    </tr>
    <tr>
      <td>ABS</td>
      <td>???</td>
      <td>???</td>
    </tr>
    <tr>
      <td>PLA</td>
      <td>???</td>
      <td>???</td>
    </tr>
    <tr>
      <td>Acryl plate</td>
      <td>1</td>
      <td>231x306 mm</td>
    </tr>
    <tr>
      <td>Metal rod</td>
      <td>2x</td>
      <td>21 x 5(diameter)mm</td>
    </tr>
    <tr>
      <td>RasberryPi</td>
      <td>1x</td>
      <td>Model B Version 3, with offical power supply</td>
    </tr>
    <tr>
      <td>Stepper motor</td>
      <td>1x</td>
      <td>???</td>
    </tr>
    <tr>
      <td>Power supply for stepper motor</td>
      <td>1x</td>
      <td>12V; 1,5A</td>
    </tr>  
    <tr>
      <td>Laser</td>
      <td>4x</td>
      <td>5mW; 650nm</td>
    </tr>
    <tr>
      <td>Photodiodes</td>
      <td>4x</td>
      <td>32 x 14mm; 3,3V-5V operating voltage</td>
    </tr>
	  <tr>
      <td>Jumper Cables</td>
      <td>???</td>
      <td>???</td>
    </tr>
    <tr>
      <td>Tube</td>
      <td>1x</td>
      <td>15mm diameter inside; 18mm diameter outside</td>
    </tr>
    <tr>
      <td>Height-adjustable feet</td>
      <td>4x</td>
      <td>50 x 50mm</td>
    </tr>
    <tr>
      <td>Marbles</td>
      <td>40x</td>
      <td>Acryl; 14mm</td>
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
- Rutsche.svg
- RutscheUndDeckel.svg


The SVG file for the acrylic material is:

- Glas.svg

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
<br>

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

<br>
At the end, when everything is glued together, you can also insert the pieces from the 3D scanner into the cutouts on the boards. The picture allows you to clearly see which item should go where, making it relatively simple to put everything together. It is recommended to use superglue to securely attach all the 3D items in place.

<details open>
<summary>Configuration:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/5800345b-8da9-4e8e-a76b-27cc53ce52bd" width="450" height="600">
</details>

<br>

### Marble lift
To bring the marbles back up to the top of the galton board we use a marble lift. It uses a piston system to stack the marbles on top of each other. First you want to make sure that you have everything in front of you. The following picture shows all the parts you need.  

<details open>
<summary>All parts:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/f1f9d594-ecbc-4fdd-8dbb-3b89befbe0d5" width="450" height="600">
</details>

There might be some parts with support structures, which were added by the 3D printer. You must remove them to be able to assemble the parts. In the pictures below you can see the support structure of the sliding part. The first picture shows the part with the support structure and the second shows it without.

<details open>
<summary>Support structre:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/173810d7-738a-42b6-9f9a-0abafc703b7f" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/b77e1374-ff14-41d7-81f9-b8f453433965" width="450" height="600">
</details>

The next step will be the trickiest, because we need to get the crankshaft in place. In the following there will be series of pictures which fit this expiration:
1. These are all the parts you need for the crankshaft (Pictures 1, 2 and 3)
2. In the fourth picture you can see how the cranshaft will be stuck together inside the sliding part. As you can see you need the connector tube and two of the angled square sticks. The short side of the sticks will go inside the connector tube. (Don't put them in yet!!! This is just for demonstration)
3. The sliding part will sit inside of the part with the two holes, we call it housing. Before you place it there (as in picutre one), we must put the connector tube inside of it (as in picture three).

<details open>
<summary>Assembling the crankshaft: Part 1:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/cd97e0a1-cc87-42bb-baa5-70b5c8ea8c53" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/611a08bd-bdb8-465e-89c4-7a13fa6b6331" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/c74290e4-0d16-411f-99d5-b437a82be122" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/9c4c7890-233d-4280-8751-1a98e083912b" width="450" height="600">
</details>
<br>

4. The next few steps are easier with a second person that helps with the process.
5. You must fit the two angled square sticks through the holes on each side of the housing, so that the angle is inside the housing. The first picture below shows it.
6. Now you must manage to stick one stick inside the connector tube.
7. The second person must now pull both sides of the housing away from each other, like in the second picture below.
8. While the second person is pulling it apart, you must connect the other stick to the connector pipe.
9. If the sticks and the pipe are stuck tight togther you must put the crankshaft brackets, as you can see on the last two pictures, on top of each crankshaft side.  
10. The assembling of the crankshaft is done.

<details open>
<summary>Assembling the crankshaft: Part 2:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/cde1e3c1-0f6a-4180-9288-2f96c7a4852e" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/6283e6f0-0572-49b1-81f4-2b7c9bf9200e" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/fce31fbd-d201-4ecf-8f32-2e75c5d376bd" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/fa367e22-b9ef-4cf9-8776-a42f398c40d8" width="450" height="600">
</details>
<br>

There are three more steps until the marble lift is done. First you must insert the piston, so that the open part of the piston fits onto the crankshaft tube inside of the sliding part. You can drop the piston from the top tough one of the holes of the housing. The second step is to slide the whole thing into the base, as you see in the first picture below. And finally put the connection for the hose on. There should be 4 pins which fit inside into the 4 holes on top of the lift. These are the connection parts between the lift itself and the hose. Now you can place the hose holder part on top of the lift aligned with the 4 pins.

<details open>
<summary>Connecting the hose:</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/60ff1ec3-f30c-465d-89ae-d1cb56d75c34" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/29f694f8-5878-42e6-a530-f26dc7734e38" width="450" height="600">
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/afc7d267-544e-4c2e-b63e-ad382d222c0b" width="450" height="600">
</details>
<br>

### Stepper motor
The stepper motor must be placed on one of the two sides of the lift. You must install the connector tube for the connection between the stepper motor and the lift. Just press the end of the crankshaft, which sticks out of the side of the lift, into the connector tube (the green part in the picture). You must do the same with the shaft of the stepper motor. If it fits tight, you need to make sure that both parts, the motor and the lift, are placed perfecly and then should be mounted to the base.

<details open>
<summary>Connecting the stepper motor</summary>
<br>
<img src="https://github.com/FabianMaas/TRNG/assets/129375472/90779872-0386-490d-8c08-e112c2e64319" width="450" height="600">
</details>
<br>

### RasberryPi
TODO
<br>

#### Circuit board
TODO
<br>

#### RasberryPi holder
TODO
<br>

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
<img src="https://github.com/FabianMaas/TRNG/assets/69453948/34980d81-b6a2-48f2-9f35-9d26d2ad0d2a" width="450" height="600">
</details>

The picture shows an aligned (below) and an unaligned (above) laser. For the top photodiode, only the power indicator light is on, but the laser signal light is off.
The acrylic glass can be added to the system. It is important that the glass is not glued or
fixed to the rest of the Galton Board.
<br>

## Improvement ideas
Since the project was developed unter the conditions of a prototype, the existing concept can be improved and expanded.

For example, a gyroscope can be used for better taring. This would attached to the Galton Board at a suitable location, aligned accordingly and integrated with this data in the code.

Another improvement can be reached by using more precise tools to cut or print the components. But this improvement needs additional resources.

Additionally, the Galton Board can be duplicated and arranged in cascade to increase the performance.
