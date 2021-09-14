import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from model import train_model
import os
from fastapi.responses import FileResponse


class Item(BaseModel):  # kế thừa từ class Basemodel và khai báo các biến
    cot1: int
    cot2: int
    cot3: int
    cot4: int
    cot5: int
    cot6: int
    cot7: int
    cot8: int
    cot9: int
    cot10: int
    cot11: int
    cot12: int
    cot13: int
    cot14: int
    cot15: int
    cot16: int
    cot17: int
    cot18: int
    cot19: int
    cot20: int


# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None


app = FastAPI()


def convert_dict_to_array(dict_input):
    converted_array = []
    for key in dict_input.keys():
        converted_array.append(dict_input[key])
    return converted_array


path = "D:\FPT\project\data_mining"


@app.get("/down/")
async def create_item():
    file_path = os.path.join(path, "trained_model_6_7_ver_3_randomforest.pickle")
    print(file_path)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename="trained_model_6_7_ver_3_randomforest.pickle")
    else:
        return {"error": "file not found"}

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    print(item_dict)
    array_input_predict = convert_dict_to_array(item_dict)
    array_input_predict = [array_input_predict]
    name_of_model = "trained_model_6_7_ver_3_randomforest.pickle"
    name_of_data = "csv/data.csv"
    print(array_input_predict)
    status, pr, pr_per, mess = train_model(name_of_data, name_of_model, array_input_predict)
    if pr == 0:
        print(mess)
    else:
        print("pr: ", pr)
        print("pr_per: ", pr_per)
        print(mess)

    return pr_per


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, debug=True)
