from typing import Literal

from pydantic import BaseModel, ConfigDict

OceanProximity = Literal["NEAR BAY", "<1H OCEAN", "INLAND", "NEAR OCEAN", "ISLAND"]


class PredictRequest(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: float
    total_rooms: float
    total_bedrooms: float
    population: float
    households: float
    median_income: float
    ocean_proximity: OceanProximity

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "longitude": -122.64,
                "latitude": 38.01,
                "housing_median_age": 36.0,
                "total_rooms": 1336.0,
                "total_bedrooms": 258.0,
                "population": 678.0,
                "households": 249.0,
                "median_income": 5.5789,
                "ocean_proximity": "NEAR OCEAN",
            }
        }
    )


class PredictResponse(BaseModel):
    house_price: float
