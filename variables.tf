variable "prefix" {
  description = "the prefix for all the resources, choose a short one"
}
variable "profile" {
  description = "Profile to run as"
}

variable "aws_region" {
  description = "Region to run as"
}

variable "env" {
  description = "Env to execute TF in"
}

variable "application_name" {
  description = "Tag Application name"
}

variable "bu" {
  description = "Tag Application BU"
}

variable "created_by" {
  description = "List of tags should be associated on all ressoruces -- Created By"
}

variable "project_id" {
  description = "List of tags should be associated on all ressoruces -- Project ID"
}

variable "application_id" {
  description = "List of tags should be associated on all ressoruces -- Application Id"
}

variable "core_id" {
  description = "List of tags should be associated on all ressoruces -- Core Id"
}

variable "dept_id" {
  description = "List of tags should be associated on all ressoruces -- Dept Id"
}



