# Doações
<table>
    <tr>
        <td> <!-- PagSeguro -->
            <h3>
                <div align="center">PagSeguro</div>
            </h3>
            <a href="https://pag.ae/bljJm47">
            <img src="https://stc.pagseguro.uol.com.br/public/img/botoes/doacoes/120x53-doar.gif"></a>
        </td>
        <td> <!-- PayPal -->
            <h3>
                <div align="center">PayPal</div>
            </h3>
            <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=7VVS675TLJHUL&lc=BR&item_name=Eracydes%20Lima%20Carvalho%20Junior&currency_code=BRL&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted">
            <img src="https://www.paypalobjects.com/pt_BR/BR/i/btn/btn_donateCC_LG.gif"></a>
        </td>
        <td> <!-- PicPay -->
            <h3>
                <div align="center">PicPay</div>
	        </h3>
            <a href="https://picpay.me/sansaoipb">
            <img src="https://lh3.googleusercontent.com/PX1pBd24_ygdLwvKMFrnUhJqGzG-YmhbYPkE8FM74qdXc-na7EqIA808F-7WAjZnvjziEESYZz2n8Ofn6WGdTrRufae_A7WbEVA5xASAUDpWNyqcVKE0GKNJrEVMBLCee5evEdrgJn8PgaI0E7qr0QDf6lTuCHI9osuziJwJ8-OTiR1JMOWLPLrw-wOW7IZ3DQCkyQECZpb_123x1K1fKNRw6cIyEWSgYRVwzX3PeljmxyH-EBOF-1wrO67-4rLP0CfbpRxJaX3pMyNlFZMLD0R6k6HvL1ax328z0qLafMwHjLPFlVEcyMkl-CFwJN9vgP37plpZ76NNruCBkj6W-MKQkvLevjcjf-Zq718N7ow8ZSlvUOCCZFJ1ieZZrLOINaMsmYGqMYpGEMME910zzAKtd-dm0IJ0TQTx_pZ0BXniK0HCvVhNHhPiYNYJGBMv_wlakLQ8XIcBdi0iIaEOFvrGSHhXEbDx6OZ9EKsvXQNoKBRwXD0Nnqxf3o-HW0U-P3pAskj3GSBa9qfvQqK-P4pxG98hYJ4st7_FA655I9n5bP-E6lIgFqvdJC8odyVfXFpHtVWfaO9_WVXowqdiXKzX9qQ9PetQNhTnJG_WgoqocmIh1FJhAYd08fonFfbmS_Hhnvi5qqxQytCqYxqWfh1elL18X8c=w120-h53-no"></a>
        </td>
    </tr>
</table>


# Zabbix Security Advisories

O "How to" foi testado no ZABBIX 6.0+ Oracle Linux/Rocky Linux/Redhat 8.0+, caso não utilize estas distros procure o pacote do google descritos para sua necessidade.


# Sumário
<ul>
	<li>
		<strong>
			<a href=#requisitos>Requisitos</a>
		</strong>
	</li>
	<li>
		<strong>
			<a href=#download-do-script>Download do script</a>
		</strong>
	</li>
	<li>
		<strong>
			<a href=#importe-o-template>Importe o Template</a>
		</strong>
	</li>
  <!--
	<li>
		<strong>
			<a href=#conclusão>Importe o Template</a>
		</strong>
	</li>
  -->
</ul>

<br>

# Requisitos

<b>0 – </b> Ter instalado Python 3.9 (ou superior) e seu respectivo "pip"<br>
<b>1 – </b> Estar logado como root<br>
<b>2 – </b> Edite o zabbix_agentX.conf para aumentar o Timeout para 30 e habilitar o comando remoto<br>
<b>3 – </b> Executar os seguintes comandos<br>

<h3>
Instale os pacotes:
</h3>

<pre><code>sudo -u zabbix pip3 install selenium webdriver_manager requests bs4 urllib3
sudo dnf install -y https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm</code></pre>


# Download do script

<pre><code>cd /usr/lib/zabbix/externalscripts
wget https://raw.githubusercontent.com/sansaoipb/Zabbix_Security/master/security.advisories.py -O security.advisories
sudo chown zabbix. security.advisories ; sudo chmod +x security.advisories</code></pre>

<b>OBS:</b><br>
Caso o local de seus scripts externos não seja "<b><u>/usr/lib/zabbix/externalscripts</u></b>", realize o ajuste no comando.


# Importe o Template

Para iniciarmos a configuração, é preciso importar o arquivo:

<blockquote><a href="https://github.com/sansaoipb/Zabbix_Security/blob/main/Template%20Zabbix%20Security%20Advisories.yaml" class="wikilink2" title="Acessar template" rel="nofollow">Template Zabbix Security Advisories.yaml</a></i></blockquote>

<b>OBS:</b><br>
<b>1 – </b>Na aba "<b><u>Macros</u></b>", faça o ajuste, no minimo, do valor da macro <b><u>{$ZBX_ADVISORY:"url"}</u></b>, as demais depende da necessidade, como no caso do diretório dos "externalscripts"<br>


<!--
# Conclusão

0 – Este script é para agilizar a análise e ficar visualmente mais agradável o recebimento dos alarmes;
<br><br>
1 - Faz uso diretamente da API do Telegram (MTProto), diferentemente da maioria (ouso até dizer todos), que usa o servidor HTTP dos BOTs, criando um ponto a mais de falha, além de ter a opção de escolher o remetente, se será um BOT ou uma conta;
<br><br>
2 - Integração API Telegram e WhatsApp: Realiza consulta para trazer informações do objeto, como Tipo (Grupo ou usuário), ID e nome (utilizado pelo script de "teste")
<br><br>
3 - Integração API ZBX (item): verificando se o item é do "tipo gráfico" (inteiro ou fracionário) para montar o gráfico se não for, ele envia somente o texto;
<br><br>
4 - Integração API ZBX (evento): Realiza ACK no evento, e insere um comentário (Pode ser desativado no arquivo de configuração);
<br><br>
5 - Existe opção de "saudação" (Bom dia, Boa tarde, Boa noite... dependendo do horário), juntamente com o nome, no caso do Telegram e "WhatsApp OpenSource", nome da pessoa, canal, ou grupo (Pode ser desativado no arquivo de configuração);
<br><br>
6 - Consegue realizar a criptografia dos campos, onde existem "informações sensíveis", como token do WhatsApp, o ID de conexão do telegram, usuário e senha do email (caso não use SMTP interno).
<br><br>
7 - Além de diversas pequenas configurações que impacta no resultado final, como:<br>
 7.1 - Flag para desconsideração do gráfico;<br>
 7.2 - Identificação e montagem do gráfico com todos os itens vinculados a trigger;<br>
 7.3 - Tratativa da data do evento, quem nunca se perguntou como alterar o padrão americano (2023.01.07) para o brasileiro (07/01/2023), a mensagem ja chega formatada;<br>
 7.4 - Tempo de gráfico personalizado... 
-->
