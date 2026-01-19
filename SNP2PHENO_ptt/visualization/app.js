// Create Babylon engine and scene
const canvas = document.getElementById("renderCanvas");
const engine = new BABYLON.Engine(canvas, true);
const scene = new BABYLON.Scene(engine);

// Camera and lights
const camera = new BABYLON.ArcRotateCamera("camera", 1.570, 1.400, 1.250, BABYLON.Vector3.Zero(), scene);
camera.minZ = 0.01; // Allows for much closer zooming
camera.attachControl(canvas, true);

// --- START: MODIFIED LIGHTING TO FIX DARKNESS ---
const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);
light.intensity = 2.5; // Was 1.0 (default)
light.groundColor = new BABYLON.Color3(0.5, 0.5, 0.5); // Add grey ground color instead of black

scene.imageProcessingConfiguration.exposure = 1.4;
scene.imageProcessingConfiguration.toneMappingEnabled = true;
// --- END: MODIFIED LIGHTING ---


// --- START: ADDED FOR CAMERA TOGGLE ---

/**
 * Toggles the camera mode between Perspective and Orthographic.
 */
function toggleCameraMode() {
  if (camera.mode === BABYLON.Camera.PERSPECTIVE_CAMERA) {
    // Switch to Orthographic
    camera.mode = BABYLON.Camera.ORTHOGRAPHIC_CAMERA;
    console.log("Switched to Orthographic Mode (Press 'P' to toggle)");

  } else {
    // Switch back to Perspective
    camera.mode = BABYLON.Camera.PERSPECTIVE_CAMERA;

    camera.orthoLeft = null;
    camera.orthoRight = null;
    camera.orthoTop = null;
    camera.orthoBottom = null;

    console.log("Switched to Perspective Mode (Press 'P' to toggle)");
  }
}

// Add a keydown listener to trigger the toggle
window.addEventListener("keydown", (event) => {
  // Use 'p' key to toggle perspective/orthographic
  if (event.key === "p" || event.key === "P") {
    toggleCameraMode();
  }
});

// --- END: ADDED FOR CAMERA TOGGLE ---


BABYLON.SceneLoader.ImportMesh("", "./", "human_presentation_hce.glb", scene, function (meshes) {
  // --- START OF TEXTURE CODE ---

  // --- ADD THIS CODE TO LOG MESHES ---
  console.log("Loaded Meshes:");
  meshes.forEach(mesh => {
    console.log(`- Mesh Name: ${mesh.name}, ID: ${mesh.id}`);
  });
  // --- END OF ADDED CODE ---

  // --- START: ADDED CODE TO DISABLE HELPER GEOMETRY ---
  console.log("Checking for helper geometry to disable...");
  meshes.forEach(mesh => {
    const meshNameLower = mesh.name.toLowerCase();

    if (meshNameLower.includes("helper") || meshNameLower.includes("joint")) {
      console.log(`Disabling helper geometry: ${mesh.name}`);
      mesh.setEnabled(false);
    }
  });
  // --- END: ADDED CODE TO DISABLE HELPER GEOMETRY ---


  // --- CODE FOR CYCLING HAIRSTYLES ---
  // Note: Hairstyle *model* cycling is still active.
  const hairNames = ["Human.short01", "Human.short04", "Human.afro01", "Human.braid01"];
  const hairMeshes = hairNames.map(name => scene.getMeshByName(name)).filter(mesh => mesh);
  let currentHairIndex = 0;
  let hairIntervalID = null; // We still need this for the *model* cycling

  if (hairMeshes.length > 0) {
    // Disable all hairstyles first
    hairMeshes.forEach(mesh => mesh.setEnabled(false));
    // Enable just the first one
    hairMeshes[currentHairIndex].setEnabled(true);

    // Start the cycling interval
    hairIntervalID = setInterval(() => {
      // Hide the current hair
      hairMeshes[currentHairIndex].setEnabled(false);
      // Move to the next index
      currentHairIndex = (currentHairIndex + 1) % hairMeshes.length;
      // Show the new current hair
      hairMeshes[currentHairIndex].setEnabled(true);
    }, 2000);
  }
  // --- END OF HAIRSTYLE CYCLING CODE ---

  // --- START: MODIFIED CODE FOR STATIC HAIR COLOR ---
  const blackColor = new BABYLON.Color3(0.08, 0.08, 0.08); // Natural Black
  let hairMaterial = null;

  // Check if we have hair meshes and if the first one has a material
  if (hairMeshes.length > 0 && hairMeshes[0].material) {
    // We assume all hair meshes share the same material
    hairMaterial = hairMeshes[0].material;

    // Set the color to black permanently
    if (hairMaterial instanceof BABYLON.PBRMaterial) {
      hairMaterial.albedoColor = blackColor;
    } else if (hairMaterial instanceof BABYLON.StandardMaterial) {
      hairMaterial.diffuseColor = blackColor;
    }
  } else {
    console.warn("Could not find hair material to set color.");
  }
  // --- END: MODIFIED CODE FOR STATIC HAIR COLOR ---



  const skinTexture = new BABYLON.Texture("./young_lightskinned_male_diffuse.png", scene);
  skinTexture.vScale = -1;
  const headMesh = scene.getMeshByName("Human");
  if (headMesh && headMesh.material instanceof BABYLON.PBRMaterial) {
    headMesh.material.albedoTexture = skinTexture;
    headMesh.material.albedoColor = new BABYLON.Color3(1, 1, 1);
  } else {
    console.warn("Could not find the head mesh or its material is not a PBRMaterial.");
  }

  // --- REVISED CAMERA TARGETING ---
  if (headMesh) {
    headMesh.computeWorldMatrix(true);
    const center = headMesh.getBoundingInfo().boundingSphere.centerWorld;
    camera.setTarget(center);
  }
  // --- END OF CAMERA TARGETING CODE ---


  // --- CAMERA SPIRAL ANIMATION ---

  const frameRate = 60;
  const durationInSeconds = 4;
  const totalFrames = frameRate * durationInSeconds;

  const finalTarget = new BABYLON.Vector3(-0.000, 1.464, 0.064);
  const finalAlpha = 14.136;
  const finalBeta = 1.481;
  const finalRadius = 0.751;

  camera.beta = 2.0;
  camera.radius = 3.5;

  const alphaAnim = new BABYLON.Animation("alphaAnim", "alpha", frameRate, BABYLON.Animation.ANIMATIONTYPE_FLOAT, BABYLON.Animation.ANIMATIONLOOPMODE_CONSTANT);
  const betaAnim = new BABYLON.Animation("betaAnim", "beta", frameRate, BABYLON.Animation.ANIMATIONTYPE_FLOAT, BABYLON.Animation.ANIMATIONLOOPMODE_CONSTANT);
  const radiusAnim = new BABYLON.Animation("radiusAnim", "radius", frameRate, BABYLON.Animation.ANIMATIONTYPE_FLOAT, BABYLON.Animation.ANIMATIONLOOPMODE_CONSTANT);
  const targetAnim = new BABYLON.Animation("targetAnim", "target", frameRate, BABYLON.Animation.ANIMATIONTYPE_VECTOR3, BABYLON.Animation.ANIMATIONLOOPMODE_CONSTANT);

  alphaAnim.setKeys([{ frame: 0, value: camera.alpha }, { frame: totalFrames, value: finalAlpha }]);
  betaAnim.setKeys([{ frame: 0, value: camera.beta }, { frame: totalFrames, value: finalBeta }]);
  radiusAnim.setKeys([{ frame: 0, value: camera.radius }, { frame: totalFrames, value: finalRadius }]);
  targetAnim.setKeys([{ frame: 0, value: camera.target }, { frame: totalFrames, value: finalTarget }]);

  const cameraAnimatable = scene.beginDirectAnimation(camera, [alphaAnim, betaAnim, radiusAnim, targetAnim], 0, totalFrames, false);

  // --- END OF CAMERA SPIRAL ANIMATION ---


  // --- START: MODIFIED CODE FOR STATIC EYE TEXTURE ---
  const eyeMesh = scene.getMeshByName("Human.high-poly");

  if (eyeMesh && eyeMesh.material instanceof BABYLON.PBRMaterial) {
    // Load just the one blue eye texture
    const blueEyeTexture = new BABYLON.Texture("./blue_eye.png", scene);
    blueEyeTexture.vScale = -1;

    // Set the texture permanently
    eyeMesh.material.albedoTexture = blueEyeTexture;
    eyeMesh.material.roughness = 0.2;

  } else {
    console.warn("Could not find the eye mesh ('Human.high-poly') or its material is not a PBRMaterial.");
  }
  // --- END: MODIFIED CODE FOR STATIC EYE TEXTURE ---


  // --- START: ADDED CODE FOR SUIT TEXTURE ---
  const suitMesh = scene.getMeshByName("Human.male_casualsuit06");

  if (suitMesh) {
    const suitTexture = new BABYLON.Texture("./male_casualsuit06_diffuse.png", scene);
    suitTexture.vScale = -1; // Match other textures

    if (suitMesh.material instanceof BABYLON.PBRMaterial) {
      suitMesh.material.albedoTexture = suitTexture;
      suitMesh.material.albedoColor = new BABYLON.Color3(1, 1, 1); // Ensure texture isn't tinted
    } else if (suitMesh.material instanceof BABYLON.StandardMaterial) {
      suitMesh.material.diffuseTexture = suitTexture;
      suitMesh.material.diffuseColor = new BABYLON.Color3(1, 1, 1); // Ensure texture isn't tinted
    } else {
      console.warn("Could not apply suit texture: Mesh material is not PBR or Standard.");
    }
  } else {
    // This warning will trigger if the mesh name is incorrect or not yet loaded
    // Check the console log at the top to verify the exact mesh name
    console.warn("Could not find suit mesh 'Human.male_casualsuit06'");
  }
  // --- END: ADDED CODE FOR SUIT TEXTURE ---


  // --- POST-ANIMATION SEQUENCE ---
  cameraAnimatable.onAnimationEnd = () => {
    setTimeout(() => {

      // --- START: REMOVED UNUSED INTERVAL CLEARS ---
      // We no longer have eye or hair *color* intervals,
      // but we still have the hair *model* interval.
      // We'll leave that one running, but you could add
      // clearInterval(hairIntervalID); here if you want
      // the hair *model* to stop cycling too.
      // --- END: REMOVED UNUSED INTERVAL CLEARS ---


      /* --- START: KLON AUSKOMMENTIERT ---
      // ... (your commented out code remains here) ...
      --- ENDE: KLON AUSKOMMENTIERT --- */

    }, 1000);
  };
  // --- END OF POST-ANIMATION SEQUENCE ---


  let found = false;
  const controlsDiv = document.getElementById("controls");

  meshes.forEach(mesh => {
    if (mesh.morphTargetManager) {
      found = true;
      for (let i = 0; i < mesh.morphTargetManager.numTargets; i++) {
        const target = mesh.morphTargetManager.getTarget(i);
        if (mesh.name === "Human" && target.name === "forehead-nubian-incr") {
          target.influence = 0;
        }
        const label = document.createElement("label");
        label.textContent = `${mesh.name} - ${target.name || `Target ${i}`}`;
        const slider = document.createElement("input");
        slider.type = "range"; slider.min = 0; slider.max = 1; slider.step = 0.01;
        slider.value = target.influence;
        slider.oninput = function () { target.influence = parseFloat(slider.value); };
        controls.appendChild(label);
        controls.appendChild(slider);
        controls.appendChild(document.createElement("br"));
      }
    }
  });

  if (!found) { alert("No morph targets found in any mesh!"); }
});

// Render loop
engine.runRenderLoop(() => {

  // --- START: ADDED FOR ORTHOGRAPHIC ZOOM ---
  if (camera.mode === BABYLON.Camera.ORTHOGRAPHIC_CAMERA) {
    const orthoSize = camera.radius;
    const aspectRatio = engine.getAspectRatio(camera);

    camera.orthoLeft = -orthoSize * aspectRatio;
    camera.orthoRight = orthoSize * aspectRatio;
    camera.orthoTop = orthoSize;
    camera.orthoBottom = -orthoSize;
  }
  // --- END: ADDED FOR ORTHOGRAPHIC ZOOM ---


  // --- UPDATE THE DEBUG PANEL ---
  const alpha_span = document.getElementById("cam-alpha");
  const beta_span = document.getElementById("cam-beta");
  const radius_span = document.getElementById("cam-radius");
  const pos_x_span = document.getElementById("cam-pos-x");
  const pos_y_span = document.getElementById("cam-pos-y");
  const pos_z_span = document.getElementById("cam-pos-z");
  const target_x_span = document.getElementById("cam-target-x");
  const target_y_span = document.getElementById("cam-target-y");
  const target_z_span = document.getElementById("cam-target-z");

  if (alpha_span && beta_span && radius_span) {
    alpha_span.textContent = camera.alpha.toFixed(3);
    beta_span.textContent = camera.beta.toFixed(3);
    radius_span.textContent = camera.radius.toFixed(3);
  }
  if (pos_x_span && pos_y_span && pos_z_span) {
    pos_x_span.textContent = camera.position.x.toFixed(3);
    pos_y_span.textContent = camera.position.y.toFixed(3);
    pos_z_span.textContent = camera.position.z.toFixed(3);
  }
  if (target_x_span && target_y_span && target_z_span) {
    target_x_span.textContent = camera.target.x.toFixed(3);
    target_y_span.textContent = camera.target.y.toFixed(3);
    target_z_span.textContent = camera.target.z.toFixed(3);
  }
  // --- END OF UPDATE BLOCK ---

  scene.render();
});

// Resize
window.addEventListener("resize", () => {
  engine.resize();
});