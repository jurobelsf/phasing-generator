<h1>Phasing Generator</h1>

<h2>Table of Contents</h2>

<ul>
  <li><a href="#description">Description</a></li>
  <li><a href="#code-overview">Code Overview</a>
    <ul>
      <li><a href="#score-function">Score Function</a></li>
      <li><a href="#monte-carlo-convergence">Monte Carlo Convergence</a></li>
    </ul>
  </li>
  <li><a href="#example">Example</a></li>
</ul>

<hr>

<h1 id="description">Description</h1>

<p>
<i>Piano Phase</i> is a famous musical work by
<a href="https://en.wikipedia.org/wiki/Steve_Reich">Steve Reich</a>.
</p>

<p>
The idea behind the piece is relatively simple: two pianists begin by playing the exact same sequence of notes. One performer keeps repeating the sequence unchanged, while the other gradually shifts out of phase by rotating the sequence over time, until both performers eventually realign.
</p>

<p>
Even though the concept is simple, the resulting texture is highly hypnotic and constantly evolving.
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=i0345c6zNfM">
    <img src="https://img.youtube.com/vi/i0345c6zNfM/maxresdefault.jpg" width="700">
  </a>
</p>

<p>
As you might imagine, the brilliance of the piece comes from the fact that not every melodic sequence sounds good when played simultaneously against all of its possible rotations. Finding a sequence that works well under every phase shift can become a very tedious task — so this project approaches the problem algorithmically.
</p>

<p>
This project is a sequence generator specifically designed to create pieces inspired by <i>Piano Phase</i>, using randomized simulation and musical scoring heuristics.
</p>

<hr>

<h1 id="code-overview">Code Overview</h1>

<p>The user provides the following inputs:</p>

<ul>
  <li>The number of notes in the sequence</li>
  <li>Whether to manually choose a musical scale or let the program select one randomly</li>
  <li>The rhythmic duration of the notes</li>
  <li>The number of simulations (<i>k</i>)</li>
</ul>

<p>
The program generates <i>k</i> random sequences and evaluates them using a custom score function that estimates how well the sequence behaves under phasing transformations.
</p>

<p>The final output includes:</p>

<ul>
  <li>A functional sequence for generating a <i>Piano Phase</i>-style piece, both as MIDI note numbers and symbolic note notation</li>
  <li>A <code>.mid</code> file ready to import into any DAW or notation software</li>
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
The interval weighting system is inspired by psychoacoustic and music-theoretical models of consonance and dissonance. Intervals are assigned continuous weights based on perceived stability, tension, and spectral roughness rather than strict tonal hierarchy.
</p>

<p>The interval score table used in the current implementation is:</p>

<table>
  <tr>
    <th>Semitone Difference</th>
    <th>Interval Name</th>
    <th>Perception</th>
    <th>Weight</th>
  </tr>
  <tr><td>0</td><td>Unison</td><td>Neutral / stable</td><td>0.60</td></tr>
  <tr><td>1</td><td>Minor Second</td><td>Tense</td><td>0.55</td></tr>
  <tr><td>2</td><td>Major Second</td><td>Open / floating</td><td>0.60</td></tr>
  <tr><td>3</td><td>Minor Third</td><td>Cold / melancholic</td><td>0.65</td></tr>
  <tr><td>4</td><td>Major Third</td><td>Bright</td><td>0.60</td></tr>
  <tr><td>5</td><td>Perfect Fourth</td><td>Stable</td><td>0.70</td></tr>
  <tr><td>6</td><td>Tritone</td><td>Ambiguous / tense</td><td>0.75</td></tr>
  <tr><td>7</td><td>Perfect Fifth</td><td>Stable</td><td>0.65</td></tr>
  <tr><td>8</td><td>Minor Sixth</td><td>Warm</td><td>0.70</td></tr>
  <tr><td>9</td><td>Major Sixth</td><td>Soft</td><td>0.65</td></tr>
  <tr><td>10</td><td>Minor Seventh</td><td>Tense</td><td>0.60</td></tr>
  <tr><td>11</td><td>Major Seventh</td><td>Sharp / unstable</td><td>0.60</td></tr>
</table>

<p>
Naturally, there is no single “correct” way to assign these weights.
</p>

<p>
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

<h2 id="monte-carlo-convergence">Monte Carlo Convergence</h2>

<p>
As expected, increasing the number of simulations generally leads to higher maximum scores, meaning that the algorithm is more likely to discover musically stronger sequences.
</p>

<p>
However, this improvement eventually reaches a point of diminishing returns, where additional simulations produce only negligible improvements in the best score found.
</p>

<p>
This behavior can be observed empirically in the convergence curves below.
</p>

<p>
Different Monte Carlo runs exhibit the same qualitative behavior, although each run reaches stagnation at a slightly different simulation count.
</p>

<p>
To formalize convergence, let
</p>

<p align="center">
<img src="https://latex.codecogs.com/png.image?\dpi{150}\Large%20S_{\max}(N)=\max\{S_1,S_2,\dots,S_N\}">
</p>

<p>
denote the best score found after <i>N</i> simulations.
</p>

<p>
We then define the score improvement over an additional window of <i>k</i> simulations as
</p>

<p align="center">
<img src="https://latex.codecogs.com/png.image?\dpi{150}\Large%20\Delta%20S=S_{\max}(N+k)-S_{\max}(N)">
</p>

<p>
where:
</p>

<ul>
  <li><i>N</i> is the current number of simulations,</li>
  <li><i>k</i> is a fixed future simulation window,</li>
  <li><i>\Delta S</i> measures the improvement in the best score after continuing the search.</li>
</ul>

<p>
We say that the algorithm has converged whenever
</p>

<p align="center">
<img src="https://latex.codecogs.com/png.image?\dpi{150}\Large%20\Delta%20S<\varepsilon">
</p>

<p>
for some sufficiently small threshold <i>\(\varepsilon > 0\)</i>.
</p>

<p>
This criterion is commonly known in Monte Carlo optimization literature as a
<b>Stagnation-based Stopping Criterion</b>.
</p>

<p>
Intuitively, it means that further simulations are no longer producing meaningful improvements in the best sequence found.
</p>

<p>
Using:
</p>

<ul>
  <li>500 independent Monte Carlo runs,</li>
  <li>a convergence window of <i>k = 500</i> simulations,</li>
  <li>and a threshold of <i>\(\varepsilon = 0.001\)</i>,</li>
</ul>

<p>
the following convergence statistics were obtained:
</p>

<ul>
  <li>Mean convergence simulation: 357.41</li>
  <li>Median convergence simulation: 302.5</li>
  <li>Standard deviation: 292.36</li>
</ul>

<p>
Since the true distribution of the convergence time is unknown, we estimate the expected convergence time using the Central Limit Theorem.
</p>

<p>
Let \(T_c\) denote the convergence simulation index obtained from each independent Monte Carlo run.
Given a sufficiently large number of runs (\(n = 500\)), the sampling distribution of the sample mean approaches a normal distribution:
</p>

<p align="center">
<img src="https://latex.codecogs.com/png.image?\dpi{150}\Large%20\bar{T}_c\approx\mathcal{N}\left(\mu,\frac{\sigma^2}{n}\right)">
</p>

<p>
Therefore, a 95% confidence interval for the expected convergence time can be constructed as:
</p>

<p align="center">
<img src="https://latex.codecogs.com/png.image?\dpi{150}\Large%20\bar{T}_c\pm1.96\frac{s}{\sqrt{n}}">
</p>

<p>
Substituting the observed statistics:
</p>

<p align="center">
<img src="https://latex.codecogs.com/png.image?\dpi{150}\Large%20357.41\pm1.96\frac{292.36}{\sqrt{500}}">
</p>

<p>
which yields:
</p>

<p align="center">
<img src="https://latex.codecogs.com/png.image?\dpi{150}\Large%20331.77\leq\mathbb{E}[T_c]\leq383.05">
</p>

<p>
Hence, we estimate the expected convergence time of the algorithm to be approximately <b>357 simulations</b>, with a 95% confidence interval ranging from approximately <b>332</b> to <b>383</b> simulations.
</p>

<hr>

<h1 id="example">Example</h1>

<p>
Below is an example generated by the algorithm and rendered using the <code>musicntwrk</code> library by
<a href="https://github.com/marcobn">@marcobn</a>.
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=ZZha3PtBrdY">
    <img src="https://img.youtube.com/vi/ZZha3PtBrdY/maxresdefault.jpg" width="700">
  </a>
</p>

<p>
The video demonstrates how a single generated sequence evolves through progressive phase shifting, creating constantly changing rhythmic and harmonic interactions from extremely limited material.
</p>

<p>
To visualize the generated phasing structure as notation and MIDI playback, see <code>visualize.py</code>.
</p>
