# hilos.io

Hilos backend test

## Setup

### Backend

```
python3 -m venv vendor
source vendor/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py test --keepdb
```

## Test description

Fix `api.test.test_flow_execution_api`.

### Models:

- `Team`: The team to which everything else belongs
- `Contact`: A contact with a phone number
- `Flow`: A conversation flow
- `FlowStep`: One step in a conversation flow. A step can be of type QUESTION, CONDITIONAL or MESSAGE.
- `FlowExecution`: An execution run
- `FlowExecutionContact`: An execution run for a specific contact
- `FlowExecutionStep`: An execution run of a specific flow step for a specific contact. If the step is of type QUESTION or CONDITIONAL there will be a result if the step was executed
