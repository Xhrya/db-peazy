resource "google_storage_bucket" "my_github_bucket" {
  name                        = "hack-team-db-peazy_tfc_bucket"
  location                    = "europe-west1"
  force_destroy               = true
  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true
}