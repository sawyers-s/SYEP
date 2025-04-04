#!/bin/bash
exec panel serve syep_explorer.py --port=$PORT --allow-websocket-origin="syep.onrender.com" --address=0.0.0.0
