# Hard bug reproduction

1. Turn the reported symptom into one observable claim. Use the boundary that can
   express it: a single function for local logic, a database or API for interactions,
   a browser for user-visible behavior. A passing check at a shallower boundary
   leaves the original failure unverified.
2. Build the fastest loop that still catches the exact symptom. Start with an
   existing test, fixture, request, or browser journey. Reduce setup, unrelated data,
   and actions while keeping the failing behavior visible.
3. Control the relevant inputs. Pin time or random seeds, isolate test data, and
   synchronize concurrent actors when possible. For intermittent failures, record
   the reproduction rate and the conditions tried. A single clean run is weak
   evidence against a race.
4. Run the repro against the faulty baseline before changing behavior when feasible.
   Record the command, revision, setup, and observed result. Change one hypothesis
   at a time. If the repro is blocked, name the missing precondition, the confidence
   of any source-based diagnosis, and the cheapest check that could resolve it.
5. Repeat the same check after the fix on the same surface. Keep it as a regression
   test if it is stable, valuable, and fits an existing test boundary. For performance
   work, compare measurements with the same workload and setup.
