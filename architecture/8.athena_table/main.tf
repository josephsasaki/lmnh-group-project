terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.89.0"
    }
  }
}

resource "aws_glue_catalog_table" "example1" {
  name          = "c16_trenet_plant_table"
  database_name = "c16_trenet_new_db"  # Replace with your Athena database name
  
  table_type = "EXTERNAL_TABLE"
  
  parameters = {
    EXTERNAL              = "TRUE"
    "skip.header.line.count" = "1"
    "classification"      = "csv"
  }

  storage_descriptor {
    location      = "s3://c16-trenet-s3/"  # Your S3 data location
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      name                  = "LazySimpleSerDe"
      serialization_library = "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe"

      parameters = {
        "field.delim" = ","
      }
    }

    columns {
      name = "plant_number"
      type = "string"
    }

    columns {
      name = "plant_last_watered"
      type = "string"
    }

    columns {
      name = "record_soil_moisture"
      type = "double"
    }

    columns {
      name = "record_temperature"
      type = "double"
    }

    columns {
      name = "record_timestamp"
      type = "timestamp"
    }

    columns {
      name = "plant_type_name"
      type = "string"
    }

    columns {
      name = "plant_type_scientific_name"
      type = "string"
    }

    columns {
      name = "plant_type_image_url"
      type = "string"
    }

    columns {
      name = "botanist_name"
      type = "string"
    }

    columns {
      name = "botanist_email"
      type = "string"
    }

    columns {
      name = "botanist_phone"
      type = "string"
    }

    columns {
      name = "city_name"
      type = "string"
    }

    columns {
      name = "city_latitude"
      type = "double"
    }

    columns {
      name = "city_longitude"
      type = "double"
    }

    columns {
      name = "country_name"
      type = "string"
    }

    columns {
      name = "country_capital"
      type = "string"
    }

    columns {
      name = "continent_name"
      type = "string"
    }
  }
}