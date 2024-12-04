Test Report Main Computer
=========================

Environnement
-------------

.. list-table::

   * - Python
     - 3.12.6
   * - Platform
     - Windows-11-10.0.26100-SP0
   * - System
     - Windows
   * - CPU
     - Unknown Processor (2.2 GHz - 24 Cores (32 Logical))
   * - RAM
     - 63.69 GB
   * - GPU
     - NVIDIA GeForce RTX 4090 Laptop GPU (Memory: 16376.0MB)

Summary
-------

67 tests collected, 67 passed ✅, 0 failed ❌ in 0:00:18s on 04/12/2024 at 10:01:28

Monitoring
----------

.. raw:: html

   <div style="position: relative; width: 100%; height: 620px; max-width: 100%; margin: 0 0 1em 0; padding:0;">
     <iframe src="Monitoring_Main_Computer.html"
             style="position: absolute; margin: 0; padding:0; width: 100%; height: 100%; border: none;">
     </iframe>
   </div>

Test Cases
----------

.. raw:: html

   <div class="test-page">

Fluorophore
^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Fluorophore
     - ✅
     - 4ms
   * - Predefined Fluorophores
     - ✅
     - 2ms

.. raw:: html

   <details>
      <summary>Log Test : Predefined Fluorophores</summary>
      <pre>GFP:<br>- Longueur d'onde (wavelength): 509 nm<br>- Intensité de base: 4000<br>- Variation maximale (delta): ±5%<br>- Scintillement (flickering): 30 ms<br><br>RFP:<br>- Longueur d'onde (wavelength): 582 nm<br>- Intensité de base: 4500<br>- Variation maximale (delta): ±10%<br>- Scintillement (flickering): 50 ms<br><br>CFP:<br>- Longueur d'onde (wavelength): 475 nm<br>- Intensité de base: 3500<br>- Variation maximale (delta): ±7%<br>- Scintillement (flickering): 40 ms<br><br>YFP:<br>- Longueur d'onde (wavelength): 527 nm<br>- Intensité de base: 3800<br>- Variation maximale (delta): ±6%<br>- Scintillement (flickering): 35 ms<br><br>Alexa488:<br>- Longueur d'onde (wavelength): 495 nm<br>- Intensité de base: 6000<br>- Variation maximale (delta): ±3%<br>- Scintillement (flickering): 25 ms</pre>
   </details>

Gui
^^^

.. list-table:: 
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Main Ui
     - ✅
     - 624ms
   * - Preference Ui
     - ✅
     - 3ms
   * - Settings Ui
     - ✅
     - 1.35s

.. raw:: html

   <details>
      <summary>Log Test : Main Ui</summary>
      <pre>New Status</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Settings Ui</summary>
      <pre>Génération en cours...<br>Génération en cours... Paramètres récupérés...<br>Settings :<br>  - Dimension :<br>    - Taille (px) : 256<br>    - Nombre de Frames : 1<br>  - Setup :<br>    - Taille des pixels (nm) : 160<br>    - Ouverture Numérique : 1.4<br>  - Fluorophore :<br>    - Longueur d'onde (nm) : 600<br>    - Intensité (lux ?) : 5000<br>    - Variation (%) : 10.0<br>    - Scintillement (ms) : 50<br>  - Structure :<br>    - Densité (molécules/µm²)  : 0.25<br>    - Ratio Astigmatisme : 2.0<br>    - Masque de répartition : [0, None]<br>    - Style de pile : [0, None]<br>  - Noise :<br>    - Intensité du bruit de fond (lux ?) : 500<br>    - Variation du bruit de fond (%) : 10.0<br>    - SNR : 10.0<br><br>Génération en cours... Paramètres récupérés... Paramétrisation effectué...<br>Génération terminée</pre>
   </details>

Gui Settings
^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Setting
     - ✅
     - 2ms
   * - Int Setting
     - ✅
     - 160ms
   * - Float Setting
     - ✅
     - 156ms
   * - Combo Setting
     - ✅
     - 158ms
   * - File Setting
     - ✅
     - 195ms
   * - Settings
     - ✅
     - 155ms
   * - Settings Pattern Management
     - ✅
     - 164ms
   * - Settings Stack Management
     - ✅
     - 154ms

.. raw:: html

   <details>
      <summary>Log Test : Settings</summary>
      <pre>Settings :<br>  - Dimension :<br>    - Taille (px) : 256<br>    - Nombre de Frames : 10<br>  - Setup :<br>    - Taille des pixels (nm) : 160<br>    - Ouverture Numérique : 1.4<br>  - Fluorophore :<br>    - Longueur d'onde (nm) : 600<br>    - Intensité (lux ?) : 5000<br>    - Variation (%) : 10.0<br>    - Scintillement (ms) : 50<br>  - Structure :<br>    - Densité (molécules/µm²)  : 0.25<br>    - Ratio Astigmatisme : 2.0<br>    - Masque de répartition : [0, None]<br>    - Style de pile : [0, None]<br>  - Noise :<br>    - Intensité du bruit de fond (lux ?) : 500<br>    - Variation du bruit de fond (%) : 10.0<br>    - SNR : 10.0</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Settings Pattern Management</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">La taille des carrés est trop élevé<br>(limite pour un échantillon de taille 256: 128</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Le nombre de rayon doit être une puissance de 2<br>Ex : 1, 2, 4, 8, 16...)</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Aucun fichier n'est spécifié.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Le fichier "filename" est introuvable.</span><span style="font-weight: bold"></span><br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Masque de répartition non reconnu</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Settings Stack Management</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Modèle non reconnu.</span><span style="font-weight: bold"></span></pre>
   </details>

Generator Noiser
^^^^^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Noiser
     - ✅
     - 91ms
   * - Noiser No Noise
     - ✅
     - 42ms
   * - Noiser Only Snr
     - ✅
     - 116ms
   * - Noiser Only Background
     - ✅
     - 25ms
   * - Noiser Black Image
     - ✅
     - 9ms

.. raw:: html

   <details>
      <summary>Log Test : Noiser</summary>
      <pre>SNR: 10, Background: 20 (± 10 %)</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Noiser Black Image</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Attention : le signal moyen est nul, impossible d'ajouter du SNR.</span><span style="font-weight: bold"></span></pre>
   </details>

Generator Sampler
^^^^^^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Sampler
     - ✅
     - 2.57s
   * - Sampler Masked
     - ✅
     - 778ms
   * - Sampler Change Params
     - ✅
     - 3ms
   * - Sampler Bad Options
     - ✅
     - 9ms

.. raw:: html

   <details>
      <summary>Log Test : Sampler</summary>
      <pre>Sampler Print : <br>size: 256, Pixel Size: 160 nm, Molecule Density : 0.25<br>Area: 1677.7216, Maximum molecule number: 419<br>Mask: Size: 256, Pattern: None, Options: No Options<br>Fluorophore: - Longueur d'onde (wavelength): 600 nm<br>- Intensité de base: 5000<br>- Variation maximale (delta): ±10%<br>- Scintillement (flickering): 50 ms<br>Noise: SNR: 10, Background: 500 (± 10 %)<br>Generation number : 2<br>Molecules générated : [419, 625]</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Sampler Change Params</summary>
      <pre>512</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Sampler Bad Options</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Le ratio d'astigmatisme doit être strictement positif, l'image sera noire.</span><span style="font-weight: bold"></span></pre>
   </details>

Generator Stackmodel
^^^^^^^^^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Stack Model Type
     - ✅
     - 1ms
   * - Pattern
     - ✅
     - 1ms

.. raw:: html

   <details>
      <summary>Log Test : Pattern</summary>
      <pre>Model: StackModelType.RANDOM, Options: No Options</pre>
   </details>

Generator Stacker
^^^^^^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Stacker
     - ✅
     - 601ms

.. raw:: html

   <details>
      <summary>Log Test : Stacker</summary>
      <pre>Model: StackModelType.RANDOM, Options: No Options<br>Sampler: size: 128, Pixel Size: 160 nm, Molecule Density : 0.25<br>Area: 419.4304, Maximum molecule number: 104<br>Mask: Size: 256, Pattern: None, Options: No Options<br>Fluorophore: - Longueur d'onde (wavelength): 600 nm<br>- Intensité de base: 5000<br>- Variation maximale (delta): ±10%<br>- Scintillement (flickering): 50 ms<br>Noise: SNR: 10, Background: 500 (± 10 %)<br>Generation number : 0<br>Model: StackModelType.RANDOM, Options: No Options<br>Sampler: size: 128, Pixel Size: 160 nm, Molecule Density : 0.25<br>Area: 419.4304, Maximum molecule number: 104<br>Mask: Size: 256, Pattern: None, Options: No Options<br>Fluorophore: - Longueur d'onde (wavelength): 600 nm<br>- Intensité de base: 5000<br>- Variation maximale (delta): ±10%<br>- Scintillement (flickering): 50 ms<br>Noise: SNR: 10, Background: 500 (± 10 %)<br>Generation number : 10</pre>
   </details>

Mask
^^^^

.. list-table:: 
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Mask
     - ✅
     - 16ms
   * - Generate Mask Stripes
     - ✅
     - 3ms
   * - Stripes Mask Options
     - ✅
     - 2ms
   * - Stripes Mask Options Bad
     - ✅
     - 1ms
   * - Generate Mask Squares
     - ✅
     - 2ms
   * - Squares Mask Options Little
     - ✅
     - 2ms
   * - Squares Mask Options Bad
     - ✅
     - 1ms
   * - Squares Mask Options Only One
     - ✅
     - 2ms
   * - Generate Mask Sun
     - ✅
     - 35ms
   * - Sun Mask Options
     - ✅
     - 11ms
   * - Sun Mask Options Bad
     - ✅
     - 1ms
   * - Generate Mask Existing Image
     - ✅
     - 2ms
   * - Existing Mask Options Bad Filename
     - ✅
     - 1ms
   * - None Mask
     - ✅
     - 2ms

.. raw:: html

   <details>
      <summary>Log Test : Mask</summary>
      <pre>Size: 128, Pattern: Bandes, Options: Lengths: [200, 100, 50, 25, 12, 6], mirrored, vertical</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Squares Mask Options Bad</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">La taille est trop grande. Masque blanc généré.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Sun Mask Options Bad</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Le nombre de rayons est introuvable ou manquant dans les options. Masque blanc généré.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Existing Mask Options Bad Filename</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Aucun fichier spécifié ou le fichier est introuvable. Masque blanc de taille 256 généré.</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : None Mask</summary>
      <pre>Test print mask setting: Size: 256, Pattern: None, Options: No Options</pre>
   </details>

Pattern
^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Pattern Type
     - ✅
     - 1ms
   * - Pattern
     - ✅
     - 1ms

.. raw:: html

   <details>
      <summary>Log Test : Pattern</summary>
      <pre>Pattern: None, Options: No Options<br>Pattern: Bandes, Options: Lengths: [200, 100, 50, 25, 12, 6], mirrored, vertical<br>Pattern: Carrés, Options: Size: 32<br>Pattern: Soleil, Options: Ray number: 8<br>Pattern: Image existante, Options: Path: </pre>
   </details>

Stack
^^^^^

.. list-table:: 
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Stack
     - ✅
     - 1ms
   * - Stack Setter Getter
     - ✅
     - 1ms
   * - Stack Save
     - ✅
     - 7ms
   * - Stack Open
     - ✅
     - 2ms
   * - Stack Open Bad File
     - ✅
     - 1ms

.. raw:: html

   <details>
      <summary>Log Test : Stack</summary>
      <pre>La pile est vide ou non initialisée.<br>Pile 3D : (2, 2, 2)<br>Contenu :<br>[[[1. 1.]<br>  [1. 1.]]<br><br> [[2. 2.]<br>  [2. 2.]]]</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Stack Setter Getter</summary>
      <pre>Pile 3D : (3, 2, 2)<br>Contenu :<br>[[[4. 4.]<br>  [4. 4.]]<br><br> [[2. 2.]<br>  [2. 2.]]<br><br> [[3. 3.]<br>  [3. 3.]]]</pre>
   </details>

Tools Fileio
^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Save Boolean Mask As Png
     - ✅
     - 37ms
   * - Save Boolean Mask As Png Bad Mask
     - ✅
     - 1ms
   * - Open Png As Boolean Mask
     - ✅
     - 2ms
   * - Open Png As Boolean Mask Bad File
     - ✅
     - 1ms
   * - Save Sample As Png
     - ✅
     - 7ms
   * - Save Sample As Png Bad Sample
     - ✅
     - 1ms
   * - Open Png As Sample
     - ✅
     - 6ms
   * - Open Png As Sample Bad File
     - ✅
     - 1ms
   * - Save Stack As Tif
     - ✅
     - 8ms
   * - Save Stack As Tif 2D
     - ✅
     - 8ms
   * - Save Stack As Tif Bad Stack
     - ✅
     - 1ms
   * - Open Tif As Stack
     - ✅
     - 5ms
   * - Open Tif As Stack Bad File
     - ✅
     - 1ms

Tools Monitoring
^^^^^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Monitoring
     - ✅
     - 1.43s
   * - Monitoring Save
     - ✅
     - 7.10s

.. raw:: html

   <details>
      <summary>Log Test : Monitoring</summary>
      <pre>6 entrées.<br>Timestamps : [0.0, 0.21, 0.43, 0.64, 0.85, 1.06]<br>CPU Usage : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]<br>Memory Usage : [203.390625, 203.39453125, 203.39453125, 203.3984375, 203.3984375, 203.375]<br>Disk Usage : [0, 0.0, 0.0, 0.0, 0.0, 0.0]</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Monitoring Save</summary>
      <pre>Simulating high CPU usage for 2 seconds...<br>CPU simulation complete.<br>Allocating 50 MB of memory...<br>Memory allocated. Holding for 2 seconds...<br>Releasing memory.<br>Writing a file of size 10 MB...<br>File written. Holding for 2 seconds...<br>Deleting the file...<br>Disk I/O simulation complete.<br><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Kaleido doesn't work so well need update. No Image Saved.</span><span style="font-weight: bold"></span></pre>
   </details>

Tools Utils
^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Test Name
     - Status
     - Duration
   * - Add Extension
     - ✅
     - 1ms
   * - Add Suffix
     - ✅
     - 1ms
   * - Get Timestamp For Files
     - ✅
     - 1ms
   * - Print Error
     - ✅
     - 1ms
   * - Print Warning
     - ✅
     - 1ms
   * - Add Grid
     - ✅
     - 6ms

.. raw:: html

   <details>
      <summary>Log Test : Get Timestamp For Files</summary>
      <pre>-20241204_100128<br>-20241204</pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Print Error</summary>
      <pre><span style="color: #aa0000"></span><span style="font-weight: bold; color: #aa0000">Message d'erreur</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   <details>
      <summary>Log Test : Print Warning</summary>
      <pre><span style="color: #aa5500"></span><span style="font-weight: bold; color: #aa5500">Message d'avertissement</span><span style="font-weight: bold"></span></pre>
   </details>

.. raw:: html

   </div>

