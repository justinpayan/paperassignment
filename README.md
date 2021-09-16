# paper_assignment
Assign papers for 692C

To run code, please clone and install https://github.com/jfinkels/birkhoff.

Then run `python assign_papers.py`. The preferences are in prefs.csv and the names of papers are in goods.txt. These can be modified at any time. prefs.csv has one person on each line, with the scores given to each paper listed after.

The script converts the numerical preferences into rankings over the full set of papers. Papers are sorted first in descending order of score for each student, then by the sum of the scores given to that paper (so ties in preference are broken by preferring those papers which fewer other students wanted).

It then computes an envy-free randomized assignment using the probabilistic serial algorithm, decomposes the randomized assignment into a distribution over deterministic assignments using the Birkhoff von Neumann decomposition, and finally samples a single assignment.
