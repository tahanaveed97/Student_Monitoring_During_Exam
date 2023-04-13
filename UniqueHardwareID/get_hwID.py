import uuid

hardware_id=''

if __name__ == '__main__':
    hardware_id=str(uuid.UUID(int=uuid.getnode()))
    print("Unique Hardware ID: ",hardware_id)
    with open("Unique Hardware ID.txt", "w") as text_file:
        text_file.write(hardware_id)