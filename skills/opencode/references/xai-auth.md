# xAI OAuth recovery

Use the installed OpenCode help and
[provider account documentation](https://opencode.ai/docs/cli/providers/).
Run diagnostics against the same server as the affected session.

1. **Classify the failure.** `invalid_grant` or a rejected refresh token may
   need renewed consent. Credit, subscription, quota, and network errors do
   not justify signing in again. Inspect only provider and account metadata;
   never export credentials, read raw tokens, or include one-time codes in
   logs or reports.
2. **Reauthorize only with consent.** Check the supported login command and
   method IDs. If `opencode auth login xai --method device` is supported, let
   the account owner complete that device flow using the intended account.
   Otherwise use the supported sign-in option. Preserve existing credentials
   while the replacement is unverified.
3. **Verify model access.** If authorized to make a request, discover an
   available xAI model. Send one minimal prompt from an empty workspace,
   without private files or tool grants, using the affected server. A
   successful sign-in message alone does not prove inference works. If the
   server still selects the old account, inspect the supported account-switch
   command and switch only when authorized.
4. **Retire obsolete credentials separately.** If explicitly authorized,
   remove only the exact identified obsolete account through the supported
   logout command. Recheck account metadata and verify the replacement again.
   Report which account and server were verified, without token material.
