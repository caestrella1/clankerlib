---
name: huh
description: Re-explain your last response in simpler, plainer words. Use when the user says "huh?", "I don't follow", "simpler please", or that an answer was too complicated.
---

# Huh

The reader didn't follow your last response. Explain it again so they do.

## Rules

1. **Start with the answer.** No "Let me simplify", "In simple terms", or apology.
2. **Give the core point in 1 to 3 sentences.**
3. **Use everyday words.** Replace jargon, or define it in a few words the first time.
4. **One idea per sentence.**
5. **Show a concrete example** instead of describing the idea in the abstract.
6. **No metaphors or comparisons.** Say the literal thing.
7. **Restructure, don't just shorten.** Drop side points, caveats, and alternatives.
8. **Offer more only if useful**, in one short line at the end.
9. **Stay at this level** for the rest of the conversation.

## Example

**Before**

> The failure stems from a race between the cache invalidation path and the write-through layer: when concurrent mutations interleave, the stale read can be served before the invalidation event propagates, so the consumer observes an inconsistent snapshot. There are several possible mitigations, including versioned keys, distributed locks, or moving to a write-behind model, each with trade-offs.

**After `huh`**

> Two saves happening at the same time can leave old data in the cache, so users briefly see the old value.
>
> For example, you save a new email address and the page still shows the old one for a few seconds.
>
> The fix is to delete the cache entry before saving, not after. Want the code?
