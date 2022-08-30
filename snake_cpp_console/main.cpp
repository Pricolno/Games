#include <stdio.h>
#include <windows.h>
#include <time.h>
#include <stdlib.h>

const int Y_MAX = 25;
const int X_MAX = 100;

void GoToXY(int x, int y);
void CursorVisible(bool visible);

enum Rotation{
    left,
    right,
    up,
    down
};

enum Assets{
    //HEAD = 'o',
    HEAD = (char)253,
    TAIL = '*',
    APPLE = (char)248
};

struct Position{
    int x;
    int y;
};

class Field{
public:
    char  field[Y_MAX][X_MAX + 1];
    void CreateBoundaries(char ch);
    void Show();
    void SpownPrice();
};

class Snake{
public:
    Snake(int length_, Rotation snakeRot_):
    length(length_), snakeRot(snakeRot_){};

    void ToStartValues();
    void Move(char field[Y_MAX][X_MAX + 1]);
    void AddTail();
    bool IsGameOver();

private:
    int length;
    Position snakePos[1000];
    Rotation snakeRot;


};

int main() {
    srand(time(NULL));
    CursorVisible(false);


    Field gameField;
    Snake snake(1, up);


    gameField.CreateBoundaries(219);
    snake.ToStartValues();

    for(int i = 0; i < 20; i++){
        gameField.SpownPrice();
    }

    while(true){
        if(snake.IsGameOver()) break;
        snake.Move(gameField.field);
        gameField.Show();

        Sleep(85);
    }

    GoToXY(0, Y_MAX);



    //go_to_xy(0, 0);
    //putchar('X');
    return 0;
}

// Работа с полем
void Field::CreateBoundaries(char ch) {
    for(int y = 0; y < Y_MAX; y++) {
        for (int x = 0; x < X_MAX; x++) {
            if (y == 0 || y == Y_MAX - 1 ||
                x == 0 || x == X_MAX - 1){
                field[y][x] = ch;
            }else{
                field[y][x] = ' ';
            }
        }
        field[y][X_MAX] = '\0';

    }
}

void Field::Show(){
    GoToXY(0, 0);
    for(int y = 0; y < Y_MAX; y++){
        printf("%s\n", field[y]);
        //printf("ALOOOO\n");
    }
}

void Field::SpownPrice(){
    int x, y;
    bool isSpawn = false;
    while(true){
        x = rand() % (X_MAX - 2) + 1;
        y = rand() % (Y_MAX - 2) + 1;
        if(x % 2 == 0) isSpawn = true;
        if(field[y][x] == HEAD || field[y][x] == TAIL) isSpawn = false;
        if(isSpawn) break;
    }

    field[y][x] = (char)248;
}
// Змейка
void Snake::ToStartValues() {
    for (int i = 0; i < length; i++) {
        snakePos[i].x = 0;
        snakePos[i].y = 0;
    }
    length = 1;
    snakePos[0] = {X_MAX / 2, Y_MAX / 2};



    GoToXY(snakePos[0].x, snakePos[0].y);

    //putchar('x');
}

void Snake::Move(char field[Y_MAX][X_MAX + 1]) {
    /*
    if (GetAsyncKeyState('W')){
        snakeRot = up;
    }else if(GetAsyncKeyState('S')){
        snakeRot = down;
    }else if(GetAsyncKeyState('A')){
        snakeRot = left;
    }else if(GetAsyncKeyState('D')){
        snakeRot = right;
    } */

    if (GetAsyncKeyState(VK_UP)){
        snakeRot = up;
    }else if(GetAsyncKeyState(VK_DOWN)){
        snakeRot = down;
    }else if(GetAsyncKeyState(VK_LEFT)){
        snakeRot = left;
    }else if(GetAsyncKeyState(VK_RIGHT)){
        snakeRot = right;
    }


    field[snakePos[length - 1].y][snakePos[length - 1].x] = ' ';

    for(int i = length; i > 0; i--){
        snakePos[i] = snakePos[i - 1];
    }

    switch (snakeRot) {
        case up:
            snakePos[0].y = snakePos[0].y - 1;
            break;

        case down:
            snakePos[0].y = snakePos[0].y + 1;
            break;

        case left:
            snakePos[0].x = snakePos[0].x - 1;
            break;

        case right:
            snakePos[0].x = snakePos[0].x + 1;
            break;

    }
    // get apple
    if(field[snakePos[0].y][snakePos[0].x] == APPLE)AddTail();
    //
    field[snakePos[0].y][snakePos[0].x] = HEAD;

    if(length > 1){
        field[snakePos[1].y][snakePos[1].x] = TAIL;
    }




}

void Snake::AddTail(){
    snakePos[length].x = snakePos[length - 1].x;
    snakePos[length].y = snakePos[length - 1].y;

    length++;
}

bool Snake::IsGameOver(){
    bool isGameOver = false;
    if(snakePos[0].x <= 0 || snakePos[0].x >= X_MAX - 1 ||
        snakePos[0].y <= 0 || snakePos[0].y >= Y_MAX - 1){
        isGameOver = true;
    }

    for(int i = 2; i < length; i++){
        if(snakePos[0].x == snakePos[i].x &&
            snakePos[0].y == snakePos[i].y){
            isGameOver = true;
            break;
        }
    }
    return isGameOver;
}
// Функция курсора
void GoToXY(int x, int y){
    COORD pos = {static_cast<SHORT>(x), static_cast<SHORT>(y)};
    HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleCursorPosition(handle, pos);
}

void CursorVisible(bool visible){
    HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_CURSOR_INFO structCursorInfo;
    GetConsoleCursorInfo(handle, &structCursorInfo);
    structCursorInfo.bVisible = visible;
    SetConsoleCursorInfo(handle, &structCursorInfo);
}





















