#!/bin/bash

cd /home/frappe/frappe-bench

# Remove existing site if exists
su frappe -c "bench drop-site site1.local --root-password tugboat"

# Remove existing app if exists
su frappe -c "bench remove-app $TUGBOAT_GITHUB_REPO"
su frappe -c "bench remove-app bloomstack_demo"

# Create new site
su frappe -c "bench new-site site1.local --mariadb-root-password tugboat --admin-password PointlessPassword123!"
su frappe -c "bench use site1.local"

# Install ERPNext into site
su frappe -c "bench install-app erpnext"

# Copy app folder and set correct ownership
cp -R /var/lib/tugboat ./apps/$TUGBOAT_GITHUB_REPO
chown -R frappe:frappe ./apps/$TUGBOAT_GITHUB_REPO

su frappe -c "printf '\n$TUGBOAT_GITHUB_REPO' >> ./sites/apps.txt"

# Install app
su frappe -c "./env/bin/pip install -e ./apps/$TUGBOAT_GITHUB_REPO"
su frappe -c "bench install-app $TUGBOAT_GITHUB_REPO"

# Get Bloomstack Demo, Bloombase apps and install them
su frappe -c "bench get-app git@github.com:DigiThinkIT/bloomstack_demo.git"
su frappe -c "bench install-app bloomstack_demo"

su frappe -c "bench get-app git@github.com:DigiThinkIT/bloombase-frappe.git"
su frappe -c "bench install-app bloombase"

su frappe -c "bench set-config google_maps_key $GOOGLE_MAPS_KEY"

# For regenerating cache
su frappe -c "bench clear-cache"

# Generate Demo Data
su frappe -c "bench execute bloomstack_demo.demo.simulate"