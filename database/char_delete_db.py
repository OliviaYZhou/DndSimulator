import psycopg2
import psycopg2.extras
conn = psycopg2.connect("dbname=dndtoolkitdb user=olivia")

def delete_status_effect(character_id, effect_name):
    cur = conn.cursor()
    cur.execute('DELETE FROM STATUS_EFFECTS WHERE CHARACTERID=(%s) AND NAME=(%s);', (character_id, effect_name))
    conn.commit()
    cur.close()
    print(f"Effect {effect_name} deleted from character {character_id}")

def delete_character(character_id):
    cur = conn.cursor()
    cur.execute('DELETE FROM BASIC_CHARACTER WHERE ID=(%s);', (character_id,))
    conn.commit()
    cur.close()
    print(f"Character {character_id} deleted")

def remove_inventory_item(character_id, item_name, amount):
    if amount <= 0:
        print(f"invalid amount 'delete {amount} items of {item_name}' from {character_id}")
        return
    
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    print("remove", character_id, item_name, amount)


    q1 = """
    SELECT ITEM_NAME, AMOUNT FROM INVENTORY_ITEMS WHERE CHARACTERID=(%s) AND ITEM_NAME=(%s);
    """
    cur.execute(q1, (character_id, item_name))
    this_item = cur.fetchone()
    if not this_item:
        print(f"Error, item {item_name} dne in inventory of {character_id}")
        return
    
    existing_amount = int(this_item["amount"])

    if existing_amount <= amount:
        cur.execute('DELETE FROM INVENTORY_ITEMS WHERE ITEM_NAME=(%s);', (item_name,))
        print(f"All of {item_name} removed from inventory of {character_id}")
    else:
        cur.execute('UPDATE INVENTORY_ITEMS SET AMOUNT = (INVENTORY_ITEMS.AMOUNT - (%s)) WHERE CHARACTERID=(%s) AND ITEM_NAME=(%s);'
        , (amount, character_id, item_name))
        print(f"{amount} of {item_name} removed from inventory of {character_id}")
    
    conn.commit()
    cur.close()
    print(f"Operation: remove from {character_id}, {amount} of {item_name}: completed")