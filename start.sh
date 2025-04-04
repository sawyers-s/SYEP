#!/bin/bash
exec bokeh serve syep_explorer.py --port=$PORT --allow-websocket-origin="syep.onrender.com"
