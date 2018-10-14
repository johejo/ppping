#!/usr/bin/env bash

PYTHON_COMMAND=python3
SCRIPT_DIR=$(cd $(dirname $0);pwd)
PARENT_DIR=$(cd $(dirname $0);cd ..;pwd)
PPPING_DIR=${PARENT_DIR}/ppping
GENERATED=${SCRIPT_DIR}/ppping

echo -e "#!/usr/bin/env ${PYTHON_COMMAND}\n\"\"\"" > ${GENERATED}
cat ${PARENT_DIR}/LICENSE >> ${GENERATED}
echo -e "\"\"\"\n" >> ${GENERATED}
cat ${PPPING_DIR}/__version__.py ${PPPING_DIR}/line.py ${PPPING_DIR}/parser.py ${PPPING_DIR}/ppping.py ${PPPING_DIR}/script.py | grep -v "from" >> ${GENERATED}
chmod +x ${GENERATED}
echo -e "\n\nif __name__ == '__main__':\n    main()\n" >> ${GENERATED}
