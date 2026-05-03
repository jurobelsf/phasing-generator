<h1>Phasing Generator</h1>

<h2>Table of Contents</h2>

<ul>
  <li><a href="#description">Description</a></li>
  <li>
    <a href="#code-overview">Code Overview</a>
    <ul>
      <li><a href="#score-function">Score Function</a></li>
    </ul>
  </li>
  <li><a href="#example">Example</a></li>
</ul>

<hr>

<h1 id="description">Description</h1>

<p>
  <i>Piano Phase</i> is a famous musical work by 
  <a href="https://en.wikipedia.org/wiki/Steve_Reich">Steve Reich</a>. 
  The idea behind the piece is relatively simple: two pianists begin by playing the exact same sequence of notes. 
  One performer keeps repeating the sequence unchanged, while the other gradually shifts out of phase by rotating the sequence over time, until both performers eventually realign.
</p>

<p>
  Even though the concept is simple, the resulting texture is highly hypnotic and constantly evolving.
</p>

<p>
  (Video of the original piece:
  <a href="https://www.youtube.com/watch?v=i0345c6zNfM&list=RDi0345c6zNfM&start_radio=1">
    Piano Phase — Steve Reich
  </a>)
</p>

<p>
  As you might imagine, the brilliance of the piece comes from the fact that not every melodic sequence sounds good when played simultaneously against all of its possible rotations. 
  Finding a sequence that works well under every phase shift can become a very tedious task — so this project approaches the problem algorithmically.
</p>

<p>
  This code is a sequence generator (a list of notes) specifically designed to create pieces inspired by <i>Piano Phase</i>, using randomized simulation and musical scoring heuristics.
</p>

<hr>

<h1 id="code-overview">Code Overview</h1>

<p>
  The user provides the following inputs:
</p>

<ul>
  <li>The number of notes in the sequence</li>
  <li>Whether to manually choose a musical scale or let the program select one randomly</li>
  <li>The rhythmic duration of the notes</li>
  <li>The number of simulations (<i>k</i>)</li>
</ul>

<p>
  The program generates <i>k</i> random sequences and evaluates them using a custom score function that estimates how well the sequence behaves under phasing transformations.
</p>

<p>
  The final output includes:
</p>

<ul>
  <li>
    A “functional” sequence for generating a <i>Piano Phase</i>-style piece, both as MIDI note numbers and symbolic note notation
  </li>

  <li>
    A <code>.mid</code> file ready to import into any DAW or notation software
  </li>
</ul>

<hr>

<h2 id="score-function">Score Function</h2>

<p>
  What does it mean for a sequence to “sound good” in this context?
</p>

<p>
  The main metric comes from assigning a score to the intervallic difference (measured in MIDI semitones) between notes played simultaneously by the two phased sequences.
</p>

<p>
  The interval weighting system is inspired by psychoacoustic and music-theoretical models of consonance and dissonance. 
  Intervals are assigned continuous weights based on perceived stability, tension, and spectral roughness rather than strict tonal hierarchy.
</p>

<p>
  The interval score table used in the current implementation is:
</p>

<table>
  <thead>
    <tr>
      <th>Semitone Difference</th>
      <th>Interval Name</th>
      <th>Perception</th>
      <th>Weight</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>0</td>
      <td>Unison</td>
      <td>Neutral / stable</td>
      <td>0.60</td>
    </tr>

    <tr>
      <td>1</td>
      <td>Minor Second</td>
      <td>Tense</td>
      <td>0.55</td>
    </tr>

    <tr>
      <td>2</td>
      <td>Major Second</td>
      <td>Open / floating</td>
      <td>0.60</td>
    </tr>

    <tr>
      <td>3</td>
      <td>Minor Third</td>
      <td>Cold / melancholic</td>
      <td>0.65</td>
    </tr>

    <tr>
      <td>4</td>
      <td>Major Third</td>
      <td>Bright</td>
      <td>0.60</td>
    </tr>

    <tr>
      <td>5</td>
      <td>Perfect Fourth</td>
      <td>Stable</td>
      <td>0.70</td>
    </tr>

    <tr>
      <td>6</td>
      <td>Tritone</td>
      <td>Ambiguous / tense</td>
      <td>0.75</td>
    </tr>

    <tr>
      <td>7</td>
      <td>Perfect Fifth</td>
      <td>Stable</td>
      <td>0.65</td>
    </tr>

    <tr>
      <td>8</td>
      <td>Minor Sixth</td>
      <td>Warm</td>
      <td>0.70</td>
    </tr>

    <tr>
      <td>9</td>
      <td>Major Sixth</td>
      <td>Soft</td>
      <td>0.65</td>
    </tr>

    <tr>
      <td>10</td>
      <td>Minor Seventh</td>
      <td>Tense</td>
      <td>0.60</td>
    </tr>

    <tr>
      <td>11</td>
      <td>Major Seventh</td>
      <td>Sharp / unstable</td>
      <td>0.60</td>
    </tr>
  </tbody>
</table>

<p>
  Naturally, there is no single “correct” way to assign these weights. 
  The interval values used here are intentionally non-tonal and were tuned empirically to generate minimalist phasing textures closer to Steve Reich’s aesthetic rather than traditional tonal harmony.
</p>

<p>
  One of the most interesting aspects of the project is that the user can freely modify these weights to create completely different musical moods — for example, making the generated material brighter, darker, more tense, more unstable, or more unpredictable.
</p>

<p>
  For users interested in experimenting further with consonance/dissonance models, I strongly recommend reading 
  <a href="https://www.researchgate.net/publication/276905584_Measuring_Musical_Consonance_and_Dissonance">
    this paper
  </a>.
</p>

<p>
  In addition to the interval weighting system, the score function also evaluates:
</p>

<ul>
  <li>Pitch variety</li>
  <li>Intervallic variety (diversity in melodic jumps)</li>
  <li>A repetition penalty to avoid excessive repeated notes</li>
</ul>

<p>
  The code is thoroughly documented so users can easily tweak the relative weights of each metric and explore different musical behaviors.
</p>

<hr>

<h1 id="example">Example</h1>

<p>
  Below is an example of a score generated using a sequence produced by the algorithm, rendered with the 
  <code>musicntwrk</code> library by 
  <a href="https://github.com/marcobn">@marcobn</a>.
</p>

<p>
  (Insert image/video here)
</p>
