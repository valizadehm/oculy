# Centralizing manipulations at the datastore level will help performing
# batch updates which will prevent getting inconsistent states in plots
# All manipulations should occurs through the datastore
# Array stored in the datastored should be marked as readonly (writable=False)
# Also keep data loaders in there