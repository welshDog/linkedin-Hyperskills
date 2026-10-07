# Demo walkthrough

This walkthrough shows the full product flow in a way that is easy to demo live.

## Demo goal

Show a founder can:

1. create a draft from a brief
2. generate multiple variants
3. score them
4. approve one
5. publish it across channels
6. see dashboard-level summary

## Sample founder profile

The repo includes a demo founder profile in `src/demo/sample_founder.py`.

It contains:

- founder identity and positioning
- audience
- tone and values
- banned phrases
- proof points
- strong hooks

This is the foundation for brand memory and trust-safe content generation.

## Sample drafts

The demo includes example drafts in `src/demo/sample_drafts.py`:

- `ADHD Hyperfocus is My Superpower`
- `Why I Open Source My ADHD Struggles`
- `The ADHD Tax is Real (But Here's How I Beat It)`

These are shaped around real founder storytelling, not generic prompt output.

## Run the demo

```bash
python -m src.demo.cli
```

You will see:

- draft created
- variants generated
- score and claim risk output
- LinkedIn payload built
- mock publish results
- analytics summary
- founder dashboard output

## Example data flow

```python
api = HyperskillsAPI()

draft = api.create_draft(
    founder_id="founder-lyndz-001",
    title="ADHD Hyperfocus is My Superpower",
    brief="Personal story about hyperfocus and shipping fast",
    platforms=["linkedin", "discord"],
)

variant = api.add_variant(draft, "I have ADHD...")
approved = api.approve_variant(draft, variant.variant_id)
results = api.publish_approved_variant(draft, variant.variant_id)
```

## What the demo proves

- founder-first brand system is viable
- workflow is structured and legible
- safety and quality checks are built in
- publishing can happen across channels using a common pipeline
- analytics can be aggregated in one dashboard

## Demo output highlights

The CLI prints output like:

- variant creation confirmation
- score for each approved variant
- claim risk status
- platform payload JSON
- publish success vs failure status
- total impressions / engagement summary

## Production next step

This should become a live onboarding and demo app where a founder can:

- paste a brief
- generate variants
- approve one
- publish to LinkedIn
- track performance

This is the cleanest path to founder validation.
