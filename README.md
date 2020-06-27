# omok AI


## overview

- 예측 네트워크와 평가 네트워크를 이용하여 트리탐색을 시행한다.
- 예측 네트워크는 오목 데이터를 통해 다음수를 예측하도록 학습되었으며 평가 네트워크는 현재의 상태에 대한 가치를 평가하도록 학습되었다.
- 5목을 두거나 4목을 막거나 43, 44(외통수) 등의 몇몇 특정 상태에서는 실수를 방지하기 위해 자체 알고리즘을 통해 둔다.
- 성능 향상을 위하여 트리탐색에서 43, 44와 같은 외통수 상태의 노드에서는 평가 네트워크의 추론 대신에 상황에 맞는 값이 노드에 메겨진다(-1 혹은 1)
- 트리탐색 120회를 기준으로 온라인 오목어플에서 1급~2단의 유저들을 상대로 3승2패의 성능을 보였다.


### state.py

- 오목 상태에 대한 데이터를 담는 클래스이다.
- 렌주룰에 따라 둘 수 없는 수들과 승패를 판정하며 자체 알고리즘 및 feature 추출에 필요한 다양한 함수들이 포함되어있다.


### game.py

- 게임을 진행시키는 클래스이다.
- 착점이 주어지면 next함수는 다음 state로 진행시킨다.


### gui.py

- pygame으로 구현된 오목게임이다.
- 모든 이미지 및 내용물은 자체제작되었다.


### train_policy.py
- 딥 컨볼루션 신경망의 형태이며 자세한 구조는 해당 파일의 코드 상단부를 참조
- 입력형태는 15x15x2의 오목판 상태이며 흑과 백의 규칙 및 전략이 서로 다르므로 각각 따로 학습시켰다.
- 흑의 예측 네트워크는 pb, 백의 예측 네트워크는 pw이다.


### train_value.py
- 구조는 예측 네트워크와 출력부를 제외하고 같다. 자세한 구조는 해당 파일의 코드 상단부를 참조
- 입력형태는 15x15x2의 오목판 상태이며 흑과 백의 규칙 및 전략이 서로 다르므로 각각 따로 학습시켰다.
- 흑의 평가 네트워크는 vb, 백의 평가 네트워크는 vw이다.


### mcts.py
- 몬테카를로 트리탐색을 수행하는 함수를 담고있다.
- mcts_action() 함수를 통해 간단하게 다음 action을 받아올 수 있으며 파라미터는 4개의 신경망 모델(pb, pw, vb, vw)과 state이다.
- MCTS_COUNT의 값을 조절하여 트리탐색의 횟수를 변경할 수 있고 PRUNING_COUNT의 값을 조절하여 트리확장 시의 노드의 갯수를 변경할 수 있다.


### predict.py
- 예측 네트워크와 평가 네트워크 추론에 사용되는 함수와 예측 네트워크를 이용하여 착수하는 함수로 구성되어있다.
- 신경망 시각화, 예상 승률 출력 / 예측 네트워크만으로 착수에 사용된다.


### test.py
- 예측 네트워크만으로 착수하는 경우와 트리탐색을 사용하여 착수하는 경우간의 성능비교를 위한 테스트 파일이다.
- 10회만 트리탐색을 시행해도 26승3패1무의 결과로 트리탐색이 우수한 성능을 보였다.


### feature.py
- 오목판의 상태에서 여러 feature들을 추출하는 함수를 담고있다.
- 눈에 띄는 성능향상을 보이지 않아 신경망의 input에 추가적인 feature들을 사용하지는 않았지만 추후 feature들을 변경하여 테스트해볼 수 있을 것이다.

