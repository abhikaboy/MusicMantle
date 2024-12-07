# Introduction

Musical Mantle is a web game that uses AI to guess a secreet artist, we support semantic search and vector search to find the artist along with the artist's name

# Setup

## Prerequisites

-   Nix
-   Python 3.10
-   Node 20.4.0

## Installation

1. [Install Nix](https://zero-to-nix.com/start/install)
    <!-- markdownlint-disable MD013 -->
    ```sh
    curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
    ```
    <!-- markdownlint-enable MD013 -->

-   Type in computer password if prompted
-   Say yes to prompt

2. cd into `nix` folder
3. Run `nix-shell`
4. cd into `backend` folder
5. `python -m uvicorn main:app --reload` to start the backend
6. cd into `frontend` folder
7. `npm install` to install the dependencies
8. `npm run dev` to start the frontend
