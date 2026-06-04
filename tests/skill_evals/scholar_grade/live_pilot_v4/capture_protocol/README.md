# Scholar-Grade Live Capture Protocol

Use one prompt packet per fixture. Do not provide hidden answer keys or fixture expectation fields during the live skill run.

After each run:

1. Save the model response as Markdown.
2. Complete the run manifest template.
3. Score the output against the hidden answer key and rubric.
4. For automated-live-capture, complete the matching trace-templates JSON, save it at the manifest trace_file path, and record trace_sha256.
5. Run the scholar-grade harness with outputs, manifests, and scores.

Automated trace templates are written under trace-templates/ for each fixture.

Capture count: 10
