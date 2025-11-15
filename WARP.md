# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is an **Obsidian vault** - a personal knowledge management system consisting of markdown files. The vault is stored in iCloud Drive and synced via Obsidian's iCloud sync.

## Architecture

- **Storage**: iCloud Drive location (`~/Library/Mobile Documents/iCloud~md~obsidian/Documents/z-work-vault`)
- **Format**: All content files are markdown (`.md`)
- **Obsidian Config**: When the vault is opened in Obsidian, a `.obsidian/` directory will be created containing app settings, plugins, and themes (currently not present as vault is new)

## Working with This Vault

### File Operations

When creating or editing markdown files:
- Use standard markdown syntax
- Obsidian supports `[[wiki-style links]]` for internal linking between notes
- Obsidian supports frontmatter (YAML metadata at the top of files)
- File paths should use forward slashes even on Windows

### Git Operations

**Viewing changes:**
```bash
git --no-pager status
git --no-pager diff
```

**Committing changes:**
```bash
git add .
git commit -m "Your commit message"
git push
```

**Note**: The `.obsidian/` directory (when it exists) contains user-specific settings. Decide whether to commit it based on whether you want to sync Obsidian settings across machines.

### Important Considerations

1. **iCloud Sync**: This vault is in iCloud Drive. Be aware of potential sync conflicts if editing files both through Obsidian and directly in the filesystem
2. **Binary Files**: Avoid committing large binary files (images, PDFs) unless necessary, as they bloat git history
3. **Gitignore**: The current `.gitignore` is templated for ecu-test workspaces and may need updating for Obsidian-specific patterns

### Typical Obsidian Patterns

- **Daily Notes**: Often stored in a `Daily Notes/` or similar directory
- **Templates**: Template files typically in a `Templates/` directory
- **Attachments**: Images and other media often in an `Attachments/` or `assets/` directory
- **Tags**: Use `#tags` inline for categorization
- **Backlinks**: Obsidian automatically tracks `[[links]]` between files
