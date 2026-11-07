# Office material and lighting study

`office-study.png` is a Blender Cycles still, not a screenshot of the live Three.js application. The editable source is `assets/office-study.blend`; reproduce it using `scripts/render_study.py`.

This study adds procedural walnut and plaster, beveled manufactured edges, detailed desk accessories, an articulated task lamp, book spines, a VR headset, printer, and stethoscope. Soft window fill and warm practical lights are rendered with AgX and denoising at 1600 × 1100.

The existing live GLB is intentionally separate. Procedural shader materials must be baked to texture maps, and mesh complexity and lighting optimized, before this scene can replace the web scene. This image is a visual review milestone, not proof of mobile runtime performance or final photorealism.
