    ITEM(Tornado.listen())
    lst = TASKS()
    lst.new_item(item)
    message = "Added" + item.title
    Tornado.say(message)
    return True
