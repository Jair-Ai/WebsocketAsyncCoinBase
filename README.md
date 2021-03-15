

# Websocket for Crypto



### Simple software to get ticks from Coinbase Match Channel, and calculate Vwap

### References:
[`vwap formula`](https://ml.pages.voltaware.com/ml-data-access/mlda.html#mlda.retrieve_smart_cables)

[`coinbase match channel`](https://docs.pro.coinbase.com/#the-matches-channel)

###Development
#### Useful commands:

Format files:
```bash
yapf -i -r --style google --no-local-style -p -vv . --exclude '.venv/*' --exclude '.tox/*'
```

Run unittests:
```bash
pytest -s -vv -x --cov-report term-missing --cov=. tests/
```


