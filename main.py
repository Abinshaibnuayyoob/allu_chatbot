from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

app = FastAPI()

@app.get("/")
async def welcome():
    return{"yay!!!": "braze amigos..., its chatbot 3.0...building the new one!!!!!"}

API_KEY = "AIzaSyDyeIC30CadRZO9JyoJ4Xqit8JavMfoGhI"

inprogress_order = {}

@app.post("/webhook")
async def webhook(request: Request, jjjrk: str = Header(None)):
    if jjjrk != API_KEY:
        return JSONResponse(content={"message": "Invalid API key"}, status_code=401)


    payload = await request.json()


    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])


    intent_handler_dict = {
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_from_order,
        'order.complete - context: ongoing-order': complete_order,
        'track order - context: ongoing-tracking': track_order
    }
    return intent_handler_dict[intent](parameters, session_id)

    #return JSONResponse(content={"fulfillmentText": "Oops!! Intent not recognized."})

def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_order:
        fulfillment_text = "Oops!! a backend error occurred!, im having a trouble in placing your order." \
                           "can you please order it again"
    else:
        current_order = inprogress_order[session_id]
        bed_items = parameters['bed-item']

        removed_items = []
        no_such_items = []

        for item in bed_items:
            if item not in current_order:
                no_such_items.append(item)

            else:
                removed_items.append(item)
                del current_order[item]
        if len(removed_items) > 0:
            fulfillment_text = f'Removed {",".join(removed_items)} from your order.'

        if len(no_such_items) > 0:
            fulfillment_text = f'Your current order does not have {",".join(no_such_items)}.'

        if len(current_order.keys()) == 0:
            fulfillment_text += " Your order is now empty!!!"
        else:
            order_str = generic_helper.get_str_from_bed_dict(current_order)
            fulfillment_text += f" Here is what is left in your order: {order_str}"
        return JSONResponse(content={
            "fulfillmentText": fulfillment_text
        })

def add_to_order(parameters: dict, session_id: str):
    bed_items = parameters['bed-item']
    quantities = parameters['number']

    if len(bed_items) != len(quantities):
        fulfillment_text = "please provide the correct quantities with the food items"
    else:
        new_bed_dict = dict(zip(bed_items, quantities))

        if session_id in inprogress_order:
            current_bed_dict = inprogress_order[session_id]
            current_bed_dict.update(new_bed_dict)
            inprogress_order[session_id] = current_bed_dict
        else:
            inprogress_order[session_id] = new_bed_dict

        order_str = generic_helper.get_str_from_bed_dict(inprogress_order[session_id])
        fulfillment_text = f"so far you 've ordered {order_str}. anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_order:
        fulfillment_text = "Sorry, i am having a trouble in placing your order. Can you please order it again?"
    else:
        order = inprogress_order[session_id]
        order_id = save_to_db(order)
        if order_id == -1:
            fulfillment_text = "Oops!! backend error!, im having a trouble in placing your order."\
                               "can you please order it again"
        else:
            order_total = db_helper.get_total_order_price(order_id)
            fulfillment_text = f"Awesome. we ve placed your order"\
                               f"here's your order id #{order_id}"\
                               f"your order total is {order_total}, which you can pay on delivery"

    del inprogress_order[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()

    for bed_item, quantity in order.items():
        rcode = db_helper.insert_order_item(
            bed_item,
            quantity,
            next_order_id
        )
        if rcode == -1:
            return -1

    db_helper.insert_order_tracking(next_order_id, "in progress")
    return next_order_id


def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['order_id'])
    order_status = db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text = f"the order status for your order id: {order_id} is {order_status}"
    else:
        fulfillment_text = f"Oops!!! No order find with order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })