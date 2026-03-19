# The Four-Color Theorem

The four-color theorem states that any planar map can be colored using at most **four colors** such that no two adjacent regions share the same color.

## Origin

**Francis Guthrie** first conjectured the theorem in **1852** while coloring a map of the counties of England. He communicated it to his brother Frederick, who passed it to the mathematician Augustus De Morgan. Despite immediate interest from the mathematical community, the problem resisted proof for over a century.

## The Proof

In **1976**, **Kenneth Appel and Wolfgang Haken** at the University of Illinois announced the first complete proof. Their strategy reduced the problem to two steps:

1. Show that every planar map must contain at least one of **1,936 unavoidable configurations**.
2. Show that each of those 1,936 configurations is *reducible* — meaning any coloring of the rest of the map can be extended through it.

Verifying reducibility for all 1,936 configurations required a computer. The calculation used approximately **1,200 hours of computer time** on an IBM 360 mainframe.

## Controversy

The Appel–Haken proof was deeply controversial because it was the first major theorem whose verification could not be checked by hand in any reasonable amount of time. It sparked a lasting debate in the mathematical community about what counts as a proof, and whether a proof that cannot be humanly verified deserves the same epistemic status as a classical proof.

A shorter, cleaner computer-assisted proof was later provided by Robertson, Sanders, Seymour, and Thomas in **1997**.
