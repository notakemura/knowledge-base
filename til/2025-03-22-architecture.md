# 2025-03-22 - architecture

## 🔍 Key Learnings

オニオンアーキテクチャ用語

- presentation
  ユーザのリクエストを受け取る。
- test
- infrastructure
  外部リソースへのアクセス。
  リポジトリを配置。
- application
  ドメイン層のクライアント。
  アプリケーションサービスを配置。
- domain
  ビジネスルール、ビジネスロジック。
  エンティティ、値オブジェクト、ドメインサービス、リポジトリのインターフェースを配置。

クリーンアーキテクチャ用語

DDD 用語

- 集約ルート
  集約の中で、唯一外部からのアクセスが許されるエントリーポイントになるオブジェクト。
- ACL（Anti Corruption Layer 腐敗防止層）
  他システムと統合する際に使用する、変換層。

OOP 用語

- カプセル化
  クラスのプロパティを private や readonly にして、外部からアクセスできないようにする。保守性・安全性向上。
- 継承
  親クラスの実装を再利用可能。DRY の実現。再利用性・統一性。
- ポリモーフィズム
  異なるクラスで、共通のインターフェースや基底クラスを通して同じメソッド名で振る舞いを変えられるようにする。拡張性・テスト性向上。
- インターフェース
  コントラクトに使用。DI 向け？
- トレイト
  オブジェクトの再利用。色んなオブジェクトで使いまわせる。
  ログ処理、バリデーション、権限チェックなど？
- 抽象クラス（アブストラクト）
  共通ロジックをベースクラスにまとめるなどの使い方。
  ベースコントローラー、共通ジョブクラスなど？
- 具象クラス
- ラッパークラス
  複雑さや結合を緩くして、保守性を上げるために使用。
  API 系や SDK、値オブジェクト的なのも？
- インプリメント
- 実体と振る舞い
  実体＝オブジェクトそのもの。エンティティ、クラスとほぼ同義？
  振る舞い＝メソッドそのもの。オブジェクト内のデータを操作すること。
- DTO
  データ受け渡し専用クラス
  別モジュールのデータを取得する時に、コントラクトとして Dto で受け渡しする。
- DTA
  データベースアクセスの抽象化

**「Modularising the Monolith by Ryuta Hamasaki」**
https://youtu.be/qsDKaO-lLdw
モジュール間のコミュニケーション
→DTO、インターフェース、イベントなどのコントラクトを使う

明確なドメイン境界を決めるのが大事。
→ これが一番難しい。ビジネスロジックの理解が必要。

モジュールをチーム間で共有するのはよくない。コンフリクトする。

モジュール間のコミュニケーション
コントラクト＝ Laravel では、DTO・インターフェースのこと。
これが無いと、モジュール A がモジュール B の詳細に依存して、密結合になっちゃう。

イベント駆動型アーキテクチャ（pub, sub とか）を使えばさらにモジュール同士を疎結合にできる
→ マイクロサービスであれば Kafka とか必要
→ モジュラーモノリスであれば Laravel に備わってるキューイングシステムで OK

異なるモジュール間で、モデルに外部キー設定するのはよくない。
同じモジュール内ならぜんぜんいい。

**「一歩ずつ成長しながら進める ZOZO の基幹システムリプレイス/Growing Stap by ...」**
https://speakerdeck.com/cocet33000/growing-stap-by-stap-zozo-backoffice-system-replacement
OK：戦略的モノリス、モジュラーモノリス
NG：Big Ball of Mud、不健康なモジュラーモノリス
→ 現状のアーキテクチャで「うまくいっていない」原因を特定して、コストに見合うのであれば、解決策を練る。

Big Ball of Mud からモジュラーモノリスへの道のり
① 境界の発見（＝境界付けられたコンテキストの発見）
②① を元にモジュールを作成
③ 機能単位でモノリスからモジュラーモノリスへ移行し、API として機能を提供
※DB は変更しない（トランザクション境界は後回し）
※基本的には、集約ごとにトランザクションを貼る。
※集約をまたいでトランザクションを貼りたい場合は、① 結果整合性 ② 集約をまたいでトランザクションを貼る の 2 通り。
※① は整合性を担保する仕組みが必要、② はトランザクション境界をコード上で表現できないのが痛い。
※境界をまたがる概念があることを認識しておく。変更のコストと相談。

デプロイを分離したい、障害を分離したいなどが無い限り、マイクロサービス化しない。

「反省 モジュラモノリス タイミーの試行錯誤と現在地」
https://speakerdeck.com/shunsugai/fan-sheng-moziyuramonorisu-taiminoshi-xing-cuo-wu-toxian-zai-di
分割したら生産性が上がる は課題としては弱い。
事業やプロダクトの課題を解決するための分割の方が推進しやすい。
→ 課題に応じた必要最低限のアーキテクチャにすべき。

## 🧪 Experiments / Examples

継承の実装例

```php
// 基底クラス（共通ロジック）
abstract class BaseApiController extends Controller
{
    protected function successResponse($data)
    {
        return response()->json([
            'status' => 'success',
            'data'   => $data
        ]);
    }

    protected function errorResponse($message, $code = 400)
    {
        return response()->json([
            'status'  => 'error',
            'message' => $message
        ], $code);
    }
}

// 実際のコントローラー
class UserController extends BaseApiController
{
    public function show($id)
    {
        $user = User::find($id);
        if (!$user) {
            return $this->errorResponse('User not found', 404);
        }

        return $this->successResponse($user);
    }
}

```

ポリモーフィズムの実装例

```php
interface NotificationChannel
{
    public function send(string $message): void;
}

class EmailNotification implements NotificationChannel
{
    public function send(string $message): void
    {
        // 実際のメール送信処理
        echo "Email sent: " . $message;
    }
}

class SlackNotification implements NotificationChannel
{
    public function send(string $message): void
    {
        // Slack APIで送信
        echo "Slack message: " . $message;
    }
}

// 利用側
class Notifier
{
    private NotificationChannel $channel;

    public function __construct(NotificationChannel $channel)
    {
        $this->channel = $channel;
    }

    public function notify(string $message): void
    {
        $this->channel->send($message);
    }
}
```

```php
// 実行例
$notifier = new Notifier(new EmailNotification());
$notifier->notify("新しいユーザーが登録されました。");

$notifier = new Notifier(new SlackNotification());
$notifier->notify("エラーが発生しました。");
```

```php

```

## 💭 Reflection

-
