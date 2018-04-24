<h1>StreetLite Project - S5</h1>

<p>Purpose: the project is to centrally manage traffic lights within a municipality. Management is done from an interface and change light cycles in real time without having to move (no need to call a technician to fix it ;p). The detection of cars on their arrival is made and is managed by the microcontroller. A button for the pedestrians is necessary to ensure their safety. A real-time system for emergency vehicles will be set up to speed up the response time in urgent situations.</p>

<pre>
Language used : Python, C/C++
Software used : Vim

  Last update : 16-04-2018
</pre>

<p>We were a team of six people in Computer Engineering.</p>

Enjoy :)

<h1>Projet StreetLite - S5</h1>

<p>But: le projet consiste à faire une gestion centralisée des feux de circulation à l’intérieur d’une municipalité. La gestion se fera à partir d’une interface et permettra de modifier les cycles des feux en temps réel sans avoir à se déplacer. La détection des automobiles à leur arriver au feu est faite et est gérée par le microcontrôleur. Un bouton pour les piétons est nécessaire dans le but d’assurer la sécurité de ces derniers. Un système en temps réel pour les véhicules d’urgence sera mis en place pour accélérer le temps de réponse lors de situations urgentes.</p>

<pre>
 Langage utilisé : Python, C/C++
Logiciel utilisé : Vim

  Mise à jour le : 16-04-2018
</pre>

<p>Nous étions une équipe de six personnes en génie informatique.</p>

Amusez-vous bien :)

<h2 id="preview">Preview / Aperçu</h2>

<h3>Prototype</h3>
<img src="/preview/prototype.png" alt="Prototype - StreetLite">
🎞😜 <a href="https://youtu.be/YMZedqIUagM">StreetLite - Video</a> 😜🎞 

<h3>Kivy Application</h3>
<img src="/preview/streetlite.png" alt="Kivy App - StreetLite">
🎞😜 <a href="https://youtu.be/X8oXd3CxgQA">StreetLite (App) - Video</a> 😜🎞 

<h2>Pssst... can I try? :D</h2>
<p>Of course!</p>

<h3>Prerequisites</h3>
<pre>
python -m venv venv
source venv/bin/activate
</pre>
<pre>
pip install cython==0.25.2
pip install -r requirements.txt
</pre>
<pre>
garden install mapview
</pre>

<h3>Additional steps for Windows</h3>
<pre>
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy.deps.gstreamer
</pre>

<h3>How to use it?</h4>
<pre>
python main.py
</pre>

You can change the value of the debug mode in the configuration file. Kivy has its own configuration file installed by default. See <a href="https://kivy.org/docs/api-kivy.config.html">Kivy Config API</a> for more details.

For instance, under Linux, the path could be `~/.kivy/config.ini`.

Please note that if you want more information about the project, you can contact me ;)

<h2>License</h2>
<pre>
MIT License

Copyright (c) 2018 s0h3ck

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
</pre>
