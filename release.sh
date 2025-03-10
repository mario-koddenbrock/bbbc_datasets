#!/bin/bash

# Ensure the script exits if any command fails
set -e

# Function to display usage
usage() {
  echo "Usage: $0 <new_version>"
  echo "Example: $0 0.2.0"
  exit 1
}

# Check if the new version is provided
if [ -z "$1" ]; then
  usage
fi

NEW_VERSION=$1

# Update the version number in setup.py
echo "Updating version to $NEW_VERSION in setup.py..."
sed -i '' "s/version=\"[^\"]*\"/version=\"$NEW_VERSION\"/" setup.py

# Commit the changes
echo "Committing changes..."
git add setup.py
git commit -m "Update to version $NEW_VERSION"

# Create a new tag
echo "Creating a new tag v$NEW_VERSION..."
git tag v$NEW_VERSION

# Push the changes and the new tag to the remote repository
echo "Pushing changes to the remote repository..."
git push origin main
git push origin v$NEW_VERSION

echo "Release process completed successfully."
