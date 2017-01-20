perm_data = {
  "JJOralCare": 
          [
  {
    "out_path": "*-*us",
    "in_path": "cpi-annual",
    "mask": "2,4"
  },
  {
    "out_path": "*-*canada",
    "in_path": "cpi-annual",
    "mask": '4,0'
  },
  {
    "out_path": "brazil*-*mouthwash",
    "in_path": "population-annual-forecast",
    "mask": "12,11,22"

  },
  {
    "out_path": "*-*mexico",
    "in_path": "cpi-annual-forecast",
    "mask": "12,11,22"

  },
  {
    "out_path": "*-*germany",
    "in_path": "cpi-annual-forecast",
    "mask": "1,12,12"

  },
  {
    "out_path": "*-*brazil",
    "in_path": "cpi-annual-forecast",
    "mask": "2,2,1"

  },
  {
    "out_path": "*-*spain",
    "in_path": "cpi-annual",
    "mask":"21,1"

  },
  {
    "out_path": "*-*italy",
    "in_path": "cpi-monthly",
    "mask":'1,2'

  },
  {
    "out_path": "*-*uk",
    "in_path": "cpi-monthly",
    "mask":'1,2'

  },
  {
    "out_path": "*-*japan",
    "in_path": "cpi-monthly",
    "mask":'1,1'

  },
  {
    "out_path": "*-*australia",
    "in_path": "cpi-annual",
    "mask":'1,0'

  },
  {
    "out_path": "us*-*mouthwash",
    "in_path": "unit_price-monthly",
    "mask":'1,1,1'

  },
  {
    "out_path": "canada*-*mouthwash",
    "in_path":  "eq_price-monthly",
    "mask":'1,1'

  }
],
  "JJLean": 
    [
      {
      "out_path": "us*-*band-aid",
      "in_path": "media-tv-monthly",
      "mask":14

      },
      {
      "out_path": "us*-*band-aid",
      "in_path": "media-digital-monthly",
      "mask":2

      },
      {
      "out_path": "us*-*band-aid*-*decorated",
      "in_path": "value-annual-forecast",
      "mask":3

      },
      {
      "out_path": "us*-*band-aid*-*decorated*-*walmart",
      "in_path": "units-monthly-forecast",
      "mask":4

      },
      {
      "out_path": "us*-*band-aid*-*premium",
      "in_path": "value",
      "mask":5
      },
      {
      "out_path": "us*-*band-aid*-*premium*-*walmart",
      "in_path": "units-monthly",
      "mask":6

      },
      {
      "out_path": "us*-*band-aid*-*premium*-*walgreens",
      "in_path": "price-monthly-forecast",
      "mask":8

      },
      {
      "out_path": "us*-*band-aid*-*premium*-*target",
      "in_path": "units-monthly",
      "mask":4
      },
      {
      "out_path": "us*-*band-aid*-*value",
      "in_path": "value-monthly-forecast",
      "mask":42
      },
      {
      "out_path": "us*-*band-aid*-*value*-*walmart",
      "in_path": "value-monthly",
      "mask":22
      },
      {
      "out_path": "us*-*band-aid*-*value*-*walgreens",
      "in_path": "units-monthly",
      "mask":6
      },
      {
      "out_path": "us*-*band-aid*-*value*-*cvs",
      "in_path": "value-monthly-forecast",
      "mask":7
      }
    ]
}

