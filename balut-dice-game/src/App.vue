<template>

  <div class="cubes">
  <div class="dice dice1" ref="diceElements">
    <div class="face front"></div>
    <div class="face back"></div>
    <div class="face top"></div>
    <div class="face bottom"></div>
    <div class="face right"></div>
    <div class="face left"></div>
  </div>

  <div class="dice dice2" ref="diceElements">
    <div class="face front"></div>
    <div class="face back"></div>
    <div class="face top"></div>
    <div class="face bottom"></div>
    <div class="face right"></div>
    <div class="face left"></div>
  </div>

  <div class="dice dice3" ref="diceElements">
    <div class="face front"></div>
    <div class="face back"></div>
    <div class="face top"></div>
    <div class="face bottom"></div>
    <div class="face right"></div>
    <div class="face left"></div>
  </div>

  <div class="dice dice4" ref="diceElements">
    <div class="face front"></div>
    <div class="face back"></div>
    <div class="face top"></div>
    <div class="face bottom"></div>
    <div class="face right"></div>
    <div class="face left"></div>
  </div>

  <div class="dice dice5" ref="diceElements">
    <div class="face front"></div>
    <div class="face back"></div>
    <div class="face top"></div>
    <div class="face bottom"></div>
    <div class="face right"></div>
    <div class="face left"></div>
  </div>
</div>

<div class="information_content">
  <div class="container">
    <div class="roll">
      <h2 class="title">Roll</h2>
      <input class="roll-input" type="number" v-model="betAmount" @input="restrictNegativeValues">
      <button class="roll-button" @click="rollDice" :disabled="rolling">ROLL</button>
    </div>
  </div>

  <div class="container">
    <h2 class="title">Result</h2>
    <p v-show="!rolling">{{ rollResult }}</p>
  </div>

  <div class="container">
    <h2 class="title">Balance</h2>
    <p v-show="!rolling">Balance: {{ balance }}</p>
  </div>

  <div class="container">
    <h2 class="title">Prices</h2>

      <a href="!#" class="content">
        <span>Pair</span>
        <span>X2</span>
      </a>

      <a href="!#" class="content" >
        <span>Full house</span>
        <span>X3</span>
      </a>

      <a href="!#" class="content" >
        <span>Straight</span>
        <span>X4</span>
      </a>

      <a href="!#" class="content">
        <span>Balut</span>
        <span>X5</span>
      </a>

      <a href="!#" class="content">
        <span>Other</span>
        <span>X0</span>
      </a>
  </div>
</div>
</template>

<script>

import axios from 'axios';

export default {
  data() {
    return {
      betAmount: 0,
      balance: 100,
      rolling: false,
      rollResult: [],
      outputResult: ''
    };
  },
  methods: {
    restrictNegativeValues() {
      if (this.betAmount < 0) {
        this.betAmount = 0;
      }
    },
    async rollDice() {
      if (this.balance < this.betAmount) {
        alert('Not enough money!');
        return;
      }
      this.balance -= this.betAmount;
      this.rolling = true;

      const dice1 = Math.floor(Math.random() * 6) + 1;
      const dice2 = Math.floor(Math.random() * 6) + 1;
      const dice3 = Math.floor(Math.random() * 6) + 1;
      const dice4 = Math.floor(Math.random() * 6) + 1;
      const dice5 = Math.floor(Math.random() * 6) + 1;

      const result = [dice1, dice2, dice3, dice4, dice5];
      const combinations = ['Straight', 'Balut', 'Full House', 'Pair'];
      const odds = [5, 4, 3, 2];

      this.outputResult = 'Rolling...';

      setTimeout(async () => {

        for (let i = 0; i < combinations.length; i++) {
          const combination = combinations[i];
          const combinationValue = this.checkCombination(result, combination);
          if (combinationValue > 1) {
            let multiplier = 0;
            switch (combinations[i]) {
              case 'Straight':
                multiplier = 4;
                break;
              case 'Balut':
                multiplier = 5;
                break;
              case 'Full House':
                multiplier = 3;
                break;
              default:
                multiplier = 1;
            }

            const winnings = this.betAmount * odds[i] * multiplier;
            this.balance += winnings;

            try {
              const response = await axios.post('http://localhost:8000/transaction', {
                name: 'Win',
                amount: winnings
              });

              this.rollResult = response.data.result;

              this.outputResult = 'You win!';
            } catch (error) {
              console.error(error);
            }

            this.rollResult = result;
            this.animateDice();

            setTimeout(() => {
              this.rolling = false;
            }, 1000);
            return;
          }
        }

        this.rollResult = result;

        this.animateDice();

        this.outputResult = 'Better luck next time!';

        setTimeout(() => {
          this.rolling = false;
        }, 1000);
      }, 1000);
    },
    checkCombination(rolls, combination) {
  switch (combination) {
    case 'Straight': {
      const sortedRolls = rolls.sort();
      const straightSequence = [1, 2, 3, 4, 5, 6];
      return JSON.stringify(sortedRolls) === JSON.stringify(straightSequence) ? 5 : 1;
    }
    case 'Balut':
      return rolls.every(roll => roll === rolls[0]) ? 4 : 1;
    case 'Full House': {
      const rollCounts = {};
      for (const roll of rolls) {
        rollCounts[roll] = (rollCounts[roll] || 0) + 1;
      }
      const values = Object.values(rollCounts);
      return values.includes(3) && values.includes(2) ? 3 : 1;
    }
    case 'Pair': {
      const pairCounts = {};
      for (const roll of rolls) {
        pairCounts[roll] = (pairCounts[roll] || 0) + 1;
      }
      const pairValues = Object.values(pairCounts);
      const hasPair = pairValues.some(count => count === 2);
      return hasPair ? 2 : 1;
    }
    default:
      return 1;
  }
},
    animateDice() {
      const diceList = document.querySelectorAll('.dice');
      diceList.forEach((dice, index) => {
        switch (this.rollResult[index]) {
          case 1:
            dice.style.transform = 'rotateX(0deg) rotateY(0deg)';
            break;
          case 2:
            dice.style.transform = 'rotateX(-90deg) rotateY(0deg)';
            break;
          case 3:
            dice.style.transform = 'rotateX(0deg) rotateY(90deg)';
            break;
          case 4:
            dice.style.transform = 'rotateX(0deg) rotateY(-90deg)';
            break;
          case 5:
            dice.style.transform = 'rotateX(90deg) rotateY(0deg)';
            break;
          case 6:
            dice.style.transform = 'rotateX(180deg) rotateY(0deg)';
            break;
        }
      });
    },
  },
};
</script>

<style>

#app {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-family: Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.information_content {
  display: flex;
}

.title {
  margin-bottom: 20px;
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 300px;
  height: 300px;
  background-color: white;
  border-radius: 20%;
  margin-right: 20px;
  box-shadow: 5px 5px 0 0 gray;
}

.roll-input {
    width: 200px;
    height: 30px;
    background-color: white;
    border: 0;
}

.roll-button {
  cursor: pointer;
    margin-top: 20px;
    padding: 6px 12px;
    color: #b33951;
    border-radius: 3px;
    font: 700 16px "Montserrat";
    border: 2px solid #b33951;
    transition: 0.4s;
}

.roll-button:hover {
  color: white;
  background-color: #b33951;
}

.re-roll__button {
  cursor: pointer;
  margin-top: 20px;
  padding: 6px 12px;
  color: #b33951;
  border-radius: 3px;
  font: 700 16px "Montserrat";
  border: 2px solid #b33951;
  transition: 0.4s;
}
.re-roll__button:hover {
  color: #fff;
  background: #b33951;
}

.content {
  display: flex;
  justify-content: space-between;
  width: 120px;
}

.content:hover {
  color: brown;
}

.cubes {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  margin-bottom: 50px;
  width: 740px;
  height: 300px;
  padding: 60px 0 40px;
  border-radius: 30px;
  background: #eeeeee;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.dice {
  position: relative;
  width: 100px;
  height: 100px;
  transform-style: preserve-3d;
  transition: 1s ease;
  margin-right: 15px;
}

@keyframes rolling {
  0% {
    transform: rotateX(0deg) rotateY(0deg);
  }
  100% {
    transform: rotateX(720deg) rotateY(180deg);
  }
}

.face {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 20px;
  border: 5px solid #f6f3f0;
  transform-style: preserve-3d;
  background: linear-gradient(145deg, #dddbd8, #fff);
}

.face::before {
  position: absolute;
  content: "";
  height: 100%;
  border-radius: 20px;
  background: #eeeeee;
  transform: translateZ(-1px);
}

.face::after {
  position: absolute;
  content: "";
  top: 50%;
  left: 50%;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #131210;
}

.front {
  transform: translateZ(50px);
}

.back {
  transform: rotateX(180deg) translateZ(50px);
}

.top {
  transform: rotateX(90deg) translateZ(50px);
}

.bottom {
  transform: rotateX(-90deg) translateZ(50px);
}

.right {
  transform: rotateY(90deg) translateZ(50px);
}

.left {
  transform: rotateY(-90deg) translateZ(50px);
}

.front::after {
  width: 30px;
  height: 30px;
  background: #f63330;
  margin: -15px 0 0 -15px;
}

.back::after {
  margin: -35px 0 0 -30px;
  box-shadow: 40px 0, 0 25px, 40px 25px, 0 50px, 40px 50px;
}

.top::after {
  margin: -30px 0 0 -30px;
  box-shadow: 40px 40px;
}

.bottom::after {
  margin: -36px 0 0 -36px;
  box-shadow: 26px 26px, 52px 52px, 52px 0, 0 52px;
}

.right::after {
  margin: -30px 0 0 -30px;
  box-shadow: 40px 0, 0 40px, 40px 40px;
}

.left::after {
  margin: -35px 0 0 -35px;
  box-shadow: 25px 25px, 50px 50px;
}

* {
  box-sizing: border-box;
}

a {
  text-decoration: none;
  color: black;
  margin-bottom: 10px;
}

p,
h1, 
h2 {
  margin: 0;
  padding: 0;
}
body {
  margin: 0;
  background-color: red;
}

</style> 




