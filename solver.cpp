#include<bits/stdc++.h>

#define pb push_back
#define endl '\n'
 
using namespace std;

//um estado e um conjunto de casas ocupadas, jogadas disponiveis e qual jogada foi feita antes dele
struct estado{
    int num[10][10];
    bool disp[10][10][10];
    int ocupado;
    int anterior[3];
};

struct sudoku{
    //numeros importantes para calcular o peso de uma jogada
    int pot5[10]={1,5,25,125,625,3125,15625,78125,390625,1953125};

    //faz as mudanças necessarias causadas por uma jogada
    void joga(estado &EST, int LIN, int COL, int NUM){
        EST.ocupado++;
        EST.num[LIN][COL]=NUM;

        for(int num=1;num<=9;num++)EST.disp[LIN][COL][num]=0;
        for(int lin=1;lin<=9;lin++)EST.disp[lin][COL][NUM]=0;
        for(int col=1;col<=9;col++)EST.disp[LIN][col][NUM]=0;
        int bi = ((LIN-1)/3)*3 + 1; // Começo da linha do bloco (1, 4 ou 7)
        int bj = ((COL-1)/3)*3 + 1; // Começo da coluna do bloco (1, 4 ou 7)
        for(int lin=bi;lin<bi+3;lin++)for(int col=bj;col<bj+3;col++)EST.disp[lin][col][NUM]=0;
    }

    bool invalido(){
        estado atual = jogadas.top();
        for(int i=1;i<=9;i++){
            vector<int>incidencia1(10,0), incidencia2(10,0), incidencia3(10,0);
            vector<int>disponivel1(10,0), disponivel2(10,0), disponivel3(10,0);
            for(int j=1;j<=9;j++){
                incidencia1[atual.num[i][j]]++;
                incidencia2[atual.num[j][i]]++;
                incidencia3[atual.num[3*(i%3) + (j%3) + 1][3*((i-1)/3) + (j-1)/3 + 1]]++;
                int condition=0;
                for(int k=1;k<=9;k++){
                    if(atual.disp[i][j][k])condition++;
                    if(atual.disp[i][j][k])disponivel1[k]++;
                    if(atual.disp[j][i][k])disponivel2[k]++;
                    if(atual.disp[3*(i%3) + (j%3) + 1][3*((i-1)/3) + (j-1)/3 + 1][k])disponivel3[k]++;
                }
                if(!condition && !atual.num[i][j])return 1;
            }

            for(int k=1;k<=9;k++){
                if(!(incidencia1[k]|disponivel1[k]) || !(incidencia2[k]|disponivel2[k]) || !(incidencia3[k]|disponivel3[k])){
                    return 1;
                }
            }
        }
        return 0;
    }

    //pega o jogo inicial a partir de um array e o coloca na pilha
    stack<estado>jogadas;
    estado inicial;
    void init(int arr[10][10]){
        inicial.ocupado=0;
        for(int i=1;i<=9;i++){
            for(int j=1;j<=9;j++){
                inicial.num[i][j]=0;
                for(int k=1;k<=9;k++)inicial.disp[i][j][k]=1;
            }
        }

        for(int i=1;i<=9;i++)for(int j=1;j<=9;j++){
            if(arr[i][j]>0){
                joga(inicial,i,j,arr[i][j]);
            }
        }
        jogadas.push(inicial);
    }

    //estima o quao boa e uma jogada
    int peso(estado &EST, int LIN, int COL, int NUM){
        int ans=0, parcial=0;

        for(int lin=1;lin<=9;lin++)if(!EST.disp[lin][COL][NUM])parcial++;
        ans+=pot5[parcial];
        parcial=0;

        for(int col=1;col<=9;col++)if(!EST.disp[LIN][col][NUM])parcial++;
        ans+=pot5[parcial];
        parcial=0;

        int bi = ((LIN-1)/3)*3 + 1;
        int bj = ((COL-1)/3)*3 + 1;
        for(int lin=bi;lin<bi+3;lin++)for(int col=bj;col<bj+3;col++)if(!EST.disp[lin][col][NUM])parcial++;
        ans+=pot5[parcial];
        parcial=0;

        for(int num=1;num<=9;num++)if(!EST.disp[LIN][COL][num])parcial++;
        ans+=pot5[parcial];

        return ans;
    }

    //resolve um tabuleiro
    void solve(){
        while(!jogadas.empty()){
            //pega o estado no topo da pilha
            estado atual=jogadas.top();

            //se o tabuleiro esta totalmente ocupado, a funcao acaba
            if(atual.ocupado==81)return;

            //variavel que indica se uma iteracao pode ser pulada
            bool passa=false;

            int candidato[3];
            candidato[0]=0;
            int max_peso=0;

            //tenta pegar a melhor jogada possivel
            for(int lin=1;lin<=9;lin++)for(int col=1;col<=9;col++)for(int num=1;num<=9;num++){
                if(atual.disp[lin][col][num]){
                    int oponente = peso(atual,lin,col,num);           
                    if(oponente>max_peso){//tenta fazer a melhor jogada possivel, e vai atualizando o candidato a jogada
                        max_peso=oponente;
                        candidato[0]=lin;
                        candidato[1]=col;
                        candidato[2]=num;
                    }
                }
            }

            //se o candidato a melhor jogada nao foi atualizado (seja por ter parado antes pelo tabuleiro ser invalido
            //ou por nao ter jogadas disponiveis), retrocede
            if(candidato[0]==0){
                int op[3];
                op[0]=atual.anterior[0];
                op[1]=atual.anterior[1];
                op[2]=atual.anterior[2];

                jogadas.pop();
                if(!jogadas.empty())jogadas.top().disp[op[0]][op[1]][op[2]]=0;
                cout<<endl;
            }else{//faz a melhor jogada, encontrada anteriormente
                jogadas.push(atual);
                joga(jogadas.top(),candidato[0],candidato[1],candidato[2]);
                jogadas.top().anterior[0]=candidato[0];
                jogadas.top().anterior[1]=candidato[1];
                jogadas.top().anterior[2]=candidato[2];

                if(invalido()){
                    jogadas.pop();
                    if(!jogadas.empty())jogadas.top().disp[candidato[0]][candidato[1]][candidato[2]]=0;
                }else{
                    continue;
                }
            }
        }
    }

    //funcao para exibir o sudoku no topo da pilha,
    //conveniente para mostrar o inicial e o resolvido
    void exibe_topo(){
        if(jogadas.empty()){
            cout<<"IMPOSSIBLE";
            return;
        }

        estado topo=jogadas.top();
        for(int i=1;i<=9;i++)for(int j=1;j<=9;j++)cout<<topo.num[i][j];
    }

};

int pior_tempo=0;
int tempo_total=0;

int main(int argc, char* argv[]){
    //otimizacao de IO
    cin.tie(0);
    ios_base::sync_with_stdio(0);

    //declara uma matriz para pegar o tabuleiro inicial, e uma string para pegar ele como um input
    int inicial[10][10];
    string ss = argv[1];

    for(int i=1;i<=9;i++)for(int j=1;j<=9;j++){
        char c;
        c=ss[9*(i-1)+j-1];
        if(c=='.')inicial[i][j]=0;
        else inicial[i][j]=c-'0';
    }

    for(int i=1;i<=9;i++){
        vector<int>incidencia1(10,0), incidencia2(10,0), incidencia3(10,0);
        for(int j=1;j<=9;j++){
            incidencia1[inicial[i][j]]++;
            incidencia2[inicial[j][i]]++;
            incidencia3[inicial[3*(i%3) + (j%3) + 1][3*((i-1)/3) + (j-1)/3 + 1]]++;
        }

        for(int j=1;j<=9;j++){
            if(incidencia1[j]>1 || incidencia2[j]>1 || incidencia3[j]>1){
                cout<<"IMPOSSIBLE";
                return 0;
            }
        }
    }

    sudoku s;
    s.init(inicial);
    if(s.invalido()){
        cout<<"IMPOSSIBLE";
        return 0;
    }
    s.solve();
    s.exibe_topo();
    
    return 0;
}

