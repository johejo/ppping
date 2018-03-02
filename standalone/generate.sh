#!/usr/bin/env bash

readonly PYTHON_COMMAND=python3
readonly SCRIPT_DIR=$(cd $(dirname $0);pwd)
readonly PARENT_DIR=$(cd $(dirname $0);cd ..;pwd)
readonly PPPING_DIR=${PARENT_DIR}/ppping
readonly GENERATED=${SCRIPT_DIR}/ppping

echo "#!/usr/bin/env ${PYTHON_COMMAND}" > ${GENERATED}
cat ${PPPING_DIR}/line.py ${PPPING_DIR}/parser.py ${PPPING_DIR}/ppping.py ${PPPING_DIR}/script.py ${PPPING_DIR}/__version__.py | grep -v "from" >> ${GENERATED}
chmod +x ${GENERATED}
echo -e "if __name__ == '__main__':\n    main()\n" >> ${GENERATED}